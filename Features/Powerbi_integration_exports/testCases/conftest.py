import os

from configparser import ConfigParser
from pathlib import Path
from common_utilities.fixtures import *

""""This file provides fixture functions for driver initialization"""

global driver


@pytest.fixture(scope="session")
def environment_settings_lookup():
    """Load settings from os.environ

            Names of environment variables:
                DIMAGIQA_URL
                DIMAGIQA_LOGIN_USERNAME
                DIMAGIQA_LOGIN_PASSWORD
                DIMAGIQA_MAIL_USERNAME
                DIMAGIQA_MAIL_PASSWORD

            See https://docs.github.com/en/actions/reference/encrypted-secrets
            for instructions on how to set them.
            """
    settings = {}
    for name in ["url", "login_username", "login_password", "staging_auth_key", "prod_auth_key"]:

        var = f"DIMAGIQA_{name.upper()}"
        if var in os.environ:
            settings[name] = os.environ[var]
    if "url" not in settings:
        env = os.environ.get("DIMAGIQA_ENV") or "staging"
        subdomain = "www" if env == "production" else env
        # updates the url with the project domain while testing in CI
        project = "a/qa-automation-prod" if env == "production" else "a/qa-automation"
        settings["url"] = f"https://{subdomain}.commcarehq.org/{project}"
    return settings


@pytest.fixture(scope="session", autouse=True)
def settings(environment_settings_lookup):
    if os.environ.get("CI") == "true":
        settings = environment_settings_lookup
        settings["CI"] = "true"
        if any(x not in settings for x in ["url", "login_username", "login_password",
                                           "staging_auth_key", "prod_auth_key"]):
            lines = environment_settings_lookup.__doc__.splitlines()
            vars_ = "\n  ".join(line.strip() for line in lines if "DIMAGIQA_" in line)
            raise RuntimeError(
                f"Environment variables not set:\n  {vars_}\n\n"
                "See https://docs.github.com/en/actions/reference/encrypted-secrets "
                "for instructions on how to set them."
            )
        return settings
    path = Path(__file__).parent.parent / "settings.cfg"
    if not path.exists():
        raise RuntimeError(
            f"Not found: {path}\n\n"
            "Copy settings-sample.cfg to settings.cfg and populate "
            "it with values for the environment you want to test."
        )
    settings = ConfigParser()
    settings.read(path)
    # updates the url with the project domain while testing in local
    if settings["default"]["url"] == "https://www.commcarehq.org/":
        settings["default"]["url"] = f"{settings['default']['url']}a/qa-automation-prod"
    else:
        settings["default"]["url"] = f"{settings['default']['url']}a/qa-automation"
    return settings["default"]

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    # Collect test counts
    passed = terminalreporter.stats.get('passed', [])
    failed = terminalreporter.stats.get('failed', [])
    error = terminalreporter.stats.get('error', [])
    skipped = terminalreporter.stats.get('skipped', [])
    xfail = terminalreporter.stats.get('xfail', [])

    env = os.environ.get("DIMAGIQA_ENV", "default_env")

    # Define the filename based on the environment
    filename = f'powerbi_test_counts_{env}.txt'

    # Write the counts to a file
    with open(filename, 'w') as f:
        f.write(f'PASSED={len(passed)}\n')
        f.write(f'FAILED={len(failed)}\n')
        f.write(f'ERROR={len(error)}\n')
        f.write(f'SKIPPED={len(skipped)}\n')
        f.write(f'XFAIL={len(xfail)}\n')

# conftest.py
import pytest
import matplotlib.pyplot as plt
import base64
from io import BytesIO

_test_stats = {}

def pytest_sessionfinish(session, exitstatus):
    """Collect stats at the end of the test session."""
    tr = session.config.pluginmanager.get_plugin("terminalreporter")
    global _test_stats
    _test_stats = {
        "passed": len(tr.stats.get("passed", [])),
        "failed": len(tr.stats.get("failed", [])),
        "skipped": len(tr.stats.get("skipped", [])),
        "error": len(tr.stats.get("error", [])),
        "xfail": len(tr.stats.get("xfail", [])),
        "reruns": len(tr.stats.get("rerun", [])),
    }
    save_summary_charts(_test_stats)

import base64

def save_summary_charts(stats):
    from pathlib import Path
    out_dir = Path("slack_charts")
    out_dir.mkdir(exist_ok=True)

    passed = stats.get("passed", 0)
    failed = stats.get("failed", 0)
    skipped = stats.get("skipped", 0)
    reruns = stats.get("reruns", 0)

    # --- Pie chart with legend ---
    pie_labels = ["Passed", "Failed", "Skipped"]
    pie_sizes = [passed, failed, skipped]
    pie_colors = ["#66bb6a", "#ef5350", "#fad000"]

    fig, ax = plt.subplots()
    wedges, texts = ax.pie(
        pie_sizes,
        labels=None,
        colors=pie_colors,
        startangle=90,
        wedgeprops=dict(width=0.4)
    )
    ax.axis("equal")
    ax.set_title("Test Summary")

    # Add legend with counts
    ax.legend(
        [f"Passed: {passed}", f"Failed: {failed}", f"Skipped: {skipped}"],
        loc="lower center",
        ncol=3,
        bbox_to_anchor=(0.5, -0.15)
    )

    fig.savefig(out_dir / "summary_pie.png", bbox_inches="tight")
    plt.close(fig)

    # --- Bar chart with labels + legend ---
    bar_path = None
    if failed > 0 or reruns > 0:   # ✅ only generate if needed
        fig, ax = plt.subplots()
        bars = ax.bar(
            ["Failed", "Reruns"],
            [failed, reruns],
            color=["#ef5350", "#ffa726"]
        )
        ax.set_ylabel("Number of Tests")
        ax.set_title("Failures and Reruns")

        # Add counts above bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.05,
                str(int(height)),
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold"
            )

        # Legend with counts
        ax.legend(
            [f"Failed: {failed}", f"Reruns: {reruns}"],
            loc="lower center",
            ncol=2,
            bbox_to_anchor=(0.5, -0.15)
        )

        bar_path = out_dir / "summary_bar.png"
        fig.savefig(bar_path, bbox_inches="tight")
        plt.close(fig)

    # --- Combine ---
    combine_charts(
        pie_path=out_dir / "summary_pie.png",
        bar_path=bar_path,
        combined_path=out_dir / "summary_combined.png"
    )


import matplotlib.pyplot as plt
from PIL import Image

def combine_charts(pie_path="slack_charts/summary_pie.png",
                   bar_path=None,
                   combined_path="slack_charts/summary_combined.png"):
    """Combine pie and bar charts side by side if bar exists, else only pie."""
    from PIL import Image

    pie = Image.open(pie_path)

    if bar_path and Path(bar_path).exists():
        bar = Image.open(bar_path)
        bar = bar.resize((bar.width * pie.height // bar.height, pie.height))
        combined = Image.new("RGB", (pie.width + bar.width, pie.height), (255, 255, 255))
        combined.paste(pie, (0, 0))
        combined.paste(bar, (pie.width, 0))
    else:
        # Only pie chart
        combined = pie.copy()

    combined.save(combined_path)
    print(f"✅ Combined chart saved to {combined_path}")



def _matplotlib_img(fig) -> str:
    """Convert a matplotlib figure to base64 string."""
    buf = BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

def pytest_html_results_summary(prefix, summary, postfix, session):
    """Inject donut pie + bar chart with reruns support (parallel-safe)."""
    tr = session.config.pluginmanager.get_plugin("terminalreporter")
    stats = tr.stats if tr and hasattr(tr, "stats") else {}

    passed  = len(stats.get("passed", []))
    failed  = len(stats.get("failed", []))
    skipped = len(stats.get("skipped", []))

    # Reruns are recorded separately by pytest-rerunfailures
    reruns = len(stats.get("rerun", []))

    # --- Donut Pie Chart (Passed, Failed, Skipped) ---
    pie_labels = ["Passed", "Failed", "Skipped"]
    pie_sizes = [passed, failed, skipped]
    pie_colors = ["#66bb6a", "#ef5350", "#fad000"]

    fig, ax = plt.subplots()
    wedges, texts = ax.pie(
        pie_sizes,
        labels=None,
        colors=pie_colors,
        startangle=90,
        wedgeprops=dict(width=0.4)
    )
    ax.axis("equal")

    # Legend below the donut
    plt.legend(
        wedges,
        [f"{l}: {v}" for l, v in zip(pie_labels, pie_sizes)],
        title="Results",
        loc="upper center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=len(pie_labels)
    )
    pie_img = _matplotlib_img(fig)

    # --- Bar Chart (Failures + Reruns) ---
    bar_img = None
    if failed > 0 or reruns > 0:
        fig, ax = plt.subplots()
        bars = ax.bar(["Failed", "Reruns"], [failed, reruns], color=["#ef5350", "#ff9933"])
        ax.set_title("Failures and Reruns")
        ax.set_ylabel("Number of Tests")
        plt.legend(
            bars,
            [f"Failed: {failed}", f"Reruns: {reruns}"],
            loc="upper center",
            bbox_to_anchor=(0.5, -0.12),
            ncol=2
        )
        bar_img = _matplotlib_img(fig)

    # --- Embed in HTML report ---
    html = "<div style='text-align:center; margin-top:20px;'>"
    html += f"<h3>Test Summary</h3><img src='data:image/png;base64,{pie_img}' style='max-width:500px;'/>"
    if bar_img:
        html += f"<h3>Failures and Reruns</h3><img src='data:image/png;base64,{bar_img}' style='max-width:500px;'/>"
    html += "</div>"

    summary.append(html)
