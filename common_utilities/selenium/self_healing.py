"""
Self-Healing Locator Engine
============================
Uses OpenAI GPT-4o to automatically find alternative locators when Selenium
element lookups fail. Integrated transparently into BasePage so all page
objects benefit without any changes.

Usage (automatic via BasePage):
    Any method in BasePage that fails with TimeoutException or
    NoSuchElementException will silently attempt to heal the locator
    before re-raising the original exception.

Environment:
    OPENAI_API_KEY  — required for healing to activate.
                      If not set, healing is skipped gracefully.

Output:
    healed_locators.json  — written to the project root after each heal,
                            so your team can see which locators need updating.
"""

import json
import logging
import os
from datetime import datetime

from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Session-level cache: (by, value) -> (by, value)
# One API call per unique failed locator per test session.
# ---------------------------------------------------------------------------
_healed_cache: dict[tuple, tuple] = {}
_healing_log: list[dict] = []

_BY_TO_STR: dict = {
    By.ID: "id",
    By.XPATH: "xpath",
    By.CSS_SELECTOR: "css selector",
    By.CLASS_NAME: "class name",
    By.NAME: "name",
    By.TAG_NAME: "tag name",
    By.LINK_TEXT: "link text",
    By.PARTIAL_LINK_TEXT: "partial link text",
}

_STR_TO_BY: dict = {
    "id": By.ID,
    "xpath": By.XPATH,
    "css selector": By.CSS_SELECTOR,
    "css": By.CSS_SELECTOR,
    "class name": By.CLASS_NAME,
    "name": By.NAME,
    "tag name": By.TAG_NAME,
    "link text": By.LINK_TEXT,
    "partial link text": By.PARTIAL_LINK_TEXT,
}


def _get_dom_context(driver, max_chars: int = 50000) -> str:
    """
    Extract a focused DOM snapshot: interactive elements and elements with
    IDs / data-attributes. Much smaller than the full document while still
    giving the AI enough signal to find the right element.
    """
    try:
        dom = driver.execute_script(
            """
            var els = document.querySelectorAll(
                '[id], [name], [data-bind], [data-action], [data-target], ' +
                '[aria-label], [aria-controls], [role], ' +
                'button, input, select, textarea, a[href], label'
            );
            var out = '';
            var seen = new Set();
            els.forEach(function(el) {
                var h = el.outerHTML;
                if (h.length < 600 && !seen.has(h)) {
                    seen.add(h);
                    out += h + '\\n';
                }
            });
            return out.substring(0, arguments[0]);
            """,
            max_chars,
        )
        if dom:
            return dom
    except Exception:
        pass

    # Fallback: raw body HTML, truncated
    try:
        raw = driver.execute_script("return document.body.outerHTML;") or ""
        return raw[:max_chars]
    except Exception as exc:
        return f"[DOM capture failed: {exc}]"


def heal_locator(driver, original_locator: tuple, context_hint: str = "") -> tuple | None:
    """
    Try to find a working alternative for *original_locator* using Claude AI.

    Parameters
    ----------
    driver           : Selenium WebDriver instance
    original_locator : (By.*, value) tuple that failed
    context_hint     : optional free-text description of the element
                       (e.g. method name or action being performed)

    Returns
    -------
    (By.*, new_value) tuple if a working alternative was found, else None.
    """
    cache_key = (original_locator[0], original_locator[1])

    # Return cached result immediately — no API call needed
    if cache_key in _healed_cache:
        logger.info("[Self-Heal] Cache hit for %s", original_locator)
        return _healed_cache[cache_key]

    # Soft-fail if openai is not installed
    try:
        import openai  # noqa: F401
    except ImportError:
        logger.warning(
            "[Self-Heal] 'openai' package not installed. "
            "Run: pip install openai"
        )
        return None

    # Soft-fail if API key is missing
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.warning("[Self-Heal] OPENAI_API_KEY not set — healing disabled.")
        return None

    by_name = _BY_TO_STR.get(original_locator[0], str(original_locator[0]))
    value = original_locator[1]
    page_url = ""
    try:
        page_url = driver.current_url
    except Exception:
        pass

    dom = _get_dom_context(driver)

    prompt = f"""You are a Selenium test automation expert. A locator FAILED to find an element on the page. Your job is to identify the correct alternative locator from the DOM snapshot.

Failed locator:
  Strategy : {by_name}
  Value    : {value}
  Page URL : {page_url}
{f"  Context  : {context_hint}" if context_hint else ""}

DOM snapshot (interactive elements and elements with identifiers):
```html
{dom}
```

Return ONLY a JSON object — no markdown fences, no explanation outside the JSON:
{{
  "by": "<id | xpath | css selector | name | class name | link text | partial link text>",
  "value": "<locator value>",
  "confidence": "<high | medium | low>",
  "reasoning": "<one concise sentence>"
}}

Locator quality rules (apply in order):
1. Prefer stable strategies: id > name > css selector > xpath
2. Never use position-based XPath (//div[2], //tr[3]/td[1], etc.)
3. Prefer data-* / aria-* / role attributes over auto-generated CSS classes
4. If the element is genuinely absent from the DOM, return:
   {{"by": null, "value": null, "confidence": "low", "reasoning": "Element not found in DOM"}}
"""

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.choices[0].message.content.strip()

        # Strip markdown fences if the model wrapped anyway
        for fence in ("```json", "```"):
            if fence in raw:
                raw = raw.split(fence, 1)[1].split("```")[0].strip()
                break

        result: dict = json.loads(raw)

        if not result.get("by") or not result.get("value"):
            logger.info(
                "[Self-Heal] AI could not identify alternative: %s",
                result.get("reasoning", "no reason given"),
            )
            return None

        new_by = _STR_TO_BY.get(result["by"].lower())
        if not new_by:
            logger.warning("[Self-Heal] Unknown strategy returned by AI: %s", result["by"])
            return None

        new_value: str = result["value"]
        new_locator = (new_by, new_value)

        # Validate: healed locator must find at least one element right now
        found = driver.find_elements(new_by, new_value)
        if not found:
            logger.warning(
                "[Self-Heal] Healed locator %s matches 0 elements — discarded.", new_locator
            )
            return None

        # ---- Success: cache and log ----
        _healed_cache[cache_key] = new_locator

        record = {
            "timestamp": datetime.now().isoformat(),
            "page_url": page_url,
            "original": {"by": by_name, "value": value},
            "healed": {"by": result["by"], "value": new_value},
            "confidence": result.get("confidence", "unknown"),
            "reasoning": result.get("reasoning", ""),
        }
        _healing_log.append(record)
        _persist_healing_log()

        print(
            f"[Self-Heal] ✓ HEALED  {by_name}='{value}'"
            f"  →  {result['by']}='{new_value}'"
            f"  |  {result.get('reasoning', '')}"
        )
        return new_locator

    except json.JSONDecodeError as exc:
        logger.error("[Self-Heal] Failed to parse AI response as JSON: %s", exc)
    except Exception as exc:
        logger.error("[Self-Heal] Unexpected error during healing: %s", exc)

    return None


def _persist_healing_log() -> None:
    """Write the current session's healing log to ``healed_locators.json``."""
    try:
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        log_path = os.path.join(root, "healed_locators.json")
        with open(log_path, "w", encoding="utf-8") as fh:
            json.dump(_healing_log, fh, indent=2)
    except Exception as exc:
        logger.warning("[Self-Heal] Could not write healed_locators.json: %s", exc)


def get_healing_summary() -> dict:
    """
    Return a structured summary of all self-healing that occurred in this
    test session. Call from conftest.py ``pytest_sessionfinish`` to include
    in your run summary.
    """
    return {
        "total_unique_healed": len(_healed_cache),
        "healed_locators": [
            {
                "original": f"{_BY_TO_STR.get(k[0], k[0])}='{k[1]}'",
                "healed": f"{_BY_TO_STR.get(v[0], v[0])}='{v[1]}'",
            }
            for k, v in _healed_cache.items()
        ],
        "full_log": _healing_log,
    }