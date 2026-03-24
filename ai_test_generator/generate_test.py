"""
generate_test.py
================
AI-powered test generator for the dimagi-qa framework.

Usage (local):
    python ai_test_generator/generate_test.py \
        --suite CaseSearch \
        --description "Login as user-1, open the Music App, search for a case by song name using text input, select the case and submit the Play Song form" \
        --output Features/CaseSearch/test_cases/test_99_generated.py

Usage (GitHub Actions):
    Triggered via workflow_dispatch - see .github/workflows/ai-test-generator.yml

Requirements:
    pip install openai

Environment variable:
    OPENAI_API_KEY   Your OpenAI API key (required)
"""

import argparse
import os
import sys
import textwrap
from pathlib import Path

# Allow running from project root or from ai_test_generator/
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

try:
    from openai import OpenAI
except ImportError:
    print("[ERROR] openai package not installed. Run: pip install openai")
    sys.exit(1)

from ai_test_generator.scanner import (
    scan_suite,
    scan_common_utilities,
    format_suite_context,
    list_suites,
    SUITES,
    ROOT as PROJECT_ROOT,
)


# ─── System prompt ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = textwrap.dedent("""
You are an expert test automation engineer for the dimagi-qa Selenium framework.
Your job is to write a complete, production-ready pytest test file from a plain English description.

## FRAMEWORK RULES (follow these exactly):

0. **Constructor signatures** – this is critical:
   Every page object class has an `INSTANTIATE AS:` line in the context below.
   You MUST use EXACTLY those arguments — no more, no less.
   Examples:
   - `INSTANTIATE AS: ReportPage(driver)`      → `page = ReportPage(driver)`         ✓
   - `INSTANTIATE AS: HomePage(driver, settings)` → `page = HomePage(driver, settings)` ✓
   - Never guess or add extra parameters like `settings` if not in the constructor.

1. **Imports** – always include:
   ```python
   import pytest
   from common_utilities.selenium.webapps import WebApps
   from common_utilities.hq_login.login_page import LoginPage
   ```
   Import page objects from the suite's test_pages folder.
   Import user input constants from the suite's user_inputs module (use the provided constants — never hardcode strings).

2. **Fixtures** – every test function takes `(driver, settings)` as arguments.
   These come from conftest.py — do NOT redefine them.

3. **Page object instantiation inside each test**:
   ```python
   webapps = WebApps(driver, settings)
   page = SomePageClass(driver)
   ```

4. **Test function naming**: `test_<number>_<short_description>` (e.g. `test_01_search_and_submit`)

5. **Docstring**: Every test must have a docstring describing the test scenario in plain English.

6. **Assertions**: Use `assert` with meaningful messages.
   Example: `assert webapps.is_present_and_displayed(locator), "Element not found"`
   Or simply verify via methods that already assert internally.

7. **Logging**: Use `print()` for step-by-step logging (the framework uses print, not logging).

8. **No hardcoded strings**: Always use constants from user_inputs classes or locally defined constants.

9. **File header**: Include a module-level docstring explaining what the file tests.

10. **Only use methods that actually exist** in the page objects provided below.
    Do not invent method names. If a method does not exist, use BasePage primitives
    (wait_to_click, wait_to_clear_and_send_keys, wait_for_element, etc.).

11. **BasePage key methods** (inherited by all page objects and WebApps):
    - wait_to_click(locator)
    - wait_to_clear_and_send_keys(locator, text)
    - wait_for_element(locator, timeout=30)
    - wait_for_disappear(locator)
    - wait_to_get_text(locator) → str
    - is_present_and_displayed(locator, timeout) → bool
    - is_displayed(locator) → bool
    - find_elements_texts(locator) → list[str]
    - js_click(locator)
    - get_element(format_string, value) → locator tuple
    - scroll_to_element(locator)
    - get_url(url)
    - select_by_text(locator, value)

12. **WebApps key methods** (navigation & form submission):
    - open_app(app_name)
    - open_menu(menu_name)
    - open_form(form_name)
    - submit_the_form()
    - search_all_cases()
    - omni_search(case_name)
    - select_case_and_continue(case_name) → list[str]
    - select_first_case_on_list_and_continue()
    - navigate_to_breadcrumb(value)
    - login_as(username)
    - clear_selections_on_case_search_page()
    - search_button_on_case_search_page()

## OUTPUT FORMAT:
Return ONLY valid Python code. No markdown fences, no explanation outside the code.
The code should be ready to save directly as a .py file and run with pytest.
""").strip()


# ─── User prompt builder ───────────────────────────────────────────────────────

def build_user_prompt(description: str, suite_context: str, output_filename: str) -> str:
    suite_name_hint = Path(output_filename).stem if output_filename else "test_generated"
    return textwrap.dedent(f"""
    Generate a complete pytest test file for the following test scenario:

    TEST DESCRIPTION:
    {description}

    OUTPUT FILE: {output_filename}

    {suite_context}

    IMPORTANT:
    - Use ONLY the page objects and methods listed above.
    - Use ONLY the user input constants listed above (or define new ones at the top of the file if needed).
    - Follow all framework rules exactly.
    - Return ONLY Python code, no markdown.
    """).strip()


# ─── Claude API call ──────────────────────────────────────────────────────────

def _load_env_file():
    """Load .env file from ai_test_generator/ if it exists."""
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


def generate_test_code(description: str, suite_name: str, output_filename: str,
                       model: str = "gpt-4o") -> str:
    _load_env_file()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY not set.")
        print("  Option 1: Create ai_test_generator/.env with OPENAI_API_KEY=your-key")
        print("  Option 2: Set environment variable OPENAI_API_KEY before running")
        sys.exit(1)

    print(f"[INFO] Scanning suite: {suite_name}")
    suite_data = scan_suite(suite_name)
    common_utils = scan_common_utilities()
    suite_context = format_suite_context(suite_data, common_utils)

    print(f"[INFO] Found {len(suite_data['page_classes'])} page object class(es)")
    print(f"[INFO] Found {len(suite_data['user_inputs'])} user input constant(s)")
    print(f"[INFO] Calling OpenAI ({model}) to generate test...")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        max_tokens=4096,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(description, suite_context, output_filename)},
        ],
    )

    return response.choices[0].message.content.strip()


# ─── Output helpers ───────────────────────────────────────────────────────────

def resolve_output_path(suite_name: str, output_arg: str | None) -> Path:
    """Determine where to write the generated test file."""
    if output_arg:
        p = Path(output_arg)
        if not p.is_absolute():
            p = PROJECT_ROOT / p
        return p

    # Auto-generate path based on suite
    suite_path = SUITES.get(suite_name)
    if not suite_path:
        return PROJECT_ROOT / "generated_test.py"

    for subdir in ["test_cases", "testCases"]:
        tests_dir = suite_path / subdir
        if tests_dir.exists():
            # Find next available test number
            existing = sorted(tests_dir.glob("test_*.py"))
            if existing:
                # Try to parse the highest test number
                nums = []
                for f in existing:
                    parts = f.stem.split("_")
                    if len(parts) >= 2 and parts[1].isdigit():
                        nums.append(int(parts[1]))
                next_num = (max(nums) + 1) if nums else 99
            else:
                next_num = 1
            return tests_dir / f"test_{next_num:02d}_ai_generated.py"

    return PROJECT_ROOT / "generated_test.py"


def write_output(code: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(code, encoding="utf-8")
    print(f"\n[SUCCESS] Test file written to: {output_path}")
    print(f"[INFO] Run with: pytest {output_path.relative_to(PROJECT_ROOT)}")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a pytest test file from a plain English description.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          # Local usage
          python ai_test_generator/generate_test.py \\
            --suite CaseSearch \\
            --description "Login as user-1, open Music App, search for Song Name, submit the form"

          # Specify custom output path
          python ai_test_generator/generate_test.py \\
            --suite HQSmokeTests \\
            --description "Verify that the Reports module shows Worker Activity report" \\
            --output HQSmokeTests/testCases/test_99_worker_activity_check.py

          # List all available suites
          python ai_test_generator/generate_test.py --list-suites
        """),
    )
    parser.add_argument(
        "--suite", "-s",
        help="Target test suite name (use --list-suites to see all options)",
    )
    parser.add_argument(
        "--description", "-d",
        help="Plain English description of the test scenario",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (relative to project root). Auto-generated if not specified.",
        default=None,
    )
    parser.add_argument(
        "--model", "-m",
        help="OpenAI model to use (default: gpt-4o)",
        default="gpt-4o",
    )
    parser.add_argument(
        "--list-suites",
        action="store_true",
        help="List all available test suites and exit",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated code to stdout instead of writing to a file",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.list_suites:
        suites = list_suites()
        print("Available test suites:")
        for s in suites:
            print(f"  - {s}")
        return

    # Support env vars for GitHub Actions usage
    suite = args.suite or os.environ.get("INPUT_SUITE")
    description = args.description or os.environ.get("INPUT_DESCRIPTION")
    output_arg = args.output or os.environ.get("INPUT_OUTPUT")

    if not suite:
        print("[ERROR] --suite is required. Use --list-suites to see available suites.")
        sys.exit(1)
    if not description:
        print("[ERROR] --description is required.")
        sys.exit(1)

    if suite not in SUITES:
        print(f"[ERROR] Unknown suite '{suite}'. Available: {', '.join(list_suites())}")
        sys.exit(1)

    output_path = resolve_output_path(suite, output_arg)

    print("=" * 60)
    print("  dimagi-qa AI Test Generator")
    print("=" * 60)
    print(f"  Suite      : {suite}")
    print(f"  Description: {description[:80]}{'...' if len(description) > 80 else ''}")
    print(f"  Output     : {output_path.relative_to(PROJECT_ROOT)}")
    print(f"  Model      : {args.model}")
    print("=" * 60)

    code = generate_test_code(
        description=description,
        suite_name=suite,
        output_filename=str(output_path.relative_to(PROJECT_ROOT)),
        model=args.model,
    )

    # Strip accidental markdown fences if model adds them
    if code.startswith("```"):
        lines = code.splitlines()
        # Remove first and last fence lines
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        code = "\n".join(lines)

    if args.dry_run:
        print("\n" + "=" * 60)
        print("GENERATED CODE (dry run — not written to file):")
        print("=" * 60)
        print(code)
    else:
        write_output(code, output_path)
        print("\nNext steps:")
        print("  1. Review the generated file and adjust any locators or inputs")
        print("  2. Make sure settings.cfg is populated for your environment")
        print(f"  3. Run: pytest {output_path.relative_to(PROJECT_ROOT)} -v")


if __name__ == "__main__":
    main()