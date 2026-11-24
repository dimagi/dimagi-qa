"""
process_testcases.py
====================
Scans all ai_testcases/ folders across every test suite, finds unprocessed
.txt files, and generates a pytest test MODULE for each one.

Each .txt file = one test module (.py file) with multiple test functions.

TXT file format (save in <Suite>/ai_testcases/<module_name>.txt):
------------------------------------------------------------------
Suite: CaseSearch

Test 1: Search by song name and submit form
1. Login as user-1
2. Open the Music App
3. Search for a case by song name using text input
4. Select the case and continue
5. Submit the Play Song form
Expected Result: Form submits successfully

Test 2: Search with no results returns empty list
1. Login as user-1
2. Open the Music App
3. Search for a non-existent song name
4. Verify the list shows empty message
Expected Result: Case list is empty

Test 3: Search using combobox filter
1. Login as user-2
2. Open the Music App
3. Filter cases using a combobox property
4. Verify filtered results appear
Expected Result: Only matching cases appear in the list
------------------------------------------------------------------

Generated output goes to: <Suite>/test_cases/test_ai_<filename>.py
  → Contains test_01_..., test_02_..., test_03_... functions

Usage:
    # Process all pending txt files across all suites
    python ai_test_generator/process_testcases.py

    # Process a specific txt file
    python ai_test_generator/process_testcases.py --file Features/CaseSearch/ai_testcases/casesearch_workflows.txt

    # Dry run - show what would be generated without writing files
    python ai_test_generator/process_testcases.py --dry-run

    # Force regenerate even if .py already exists
    python ai_test_generator/process_testcases.py --force
"""

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from ai_test_generator.generate_test import generate_test_code, _load_env_file
from ai_test_generator.scanner import SUITES, list_suites

# Map suite folder paths back to suite names for auto-detection
SUITE_PATH_TO_NAME = {str(v.resolve()): k for k, v in SUITES.items()}


def detect_suite_from_path(txt_path: Path) -> str | None:
    """Detect suite name by matching the txt file's parent folders against known suite paths."""
    for parent in txt_path.parents:
        resolved = str(parent.resolve())
        if resolved in SUITE_PATH_TO_NAME:
            return SUITE_PATH_TO_NAME[resolved]
    return None


def parse_txt_file(txt_path: Path) -> dict:
    """
    Parse a test case .txt file supporting multiple test cases per file.

    Returns:
    {
        "suite": str,
        "module_name": str,
        "tests": [
            {
                "name": str,
                "tags": list,     # e.g. ["report", "smoke"]
                "steps": list,
                "expected": str,
            },
            ...
        ]
    }
    """
    content = txt_path.read_text(encoding="utf-8", errors="ignore").strip()
    lines = content.splitlines()

    suite = None
    tests = []
    current_test = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Suite header
        if stripped.lower().startswith("suite:"):
            suite = stripped.split(":", 1)[1].strip()
            continue

        # New test block: "Test 1:", "Test 2:", "Test:", etc.
        test_header = re.match(r'^test\s*\d*\s*:\s*(.+)$', stripped, re.IGNORECASE)
        if test_header:
            if current_test:
                tests.append(current_test)
            current_test = {
                "name": test_header.group(1).strip(),
                "tags": [],
                "steps": [],
                "expected": "",
            }
            continue

        # Tags line (within a test block): "Tags: report, smoke"
        if current_test and re.match(r'^tags?\s*:', stripped, re.IGNORECASE):
            raw_tags = stripped.split(":", 1)[1].strip()
            current_test["tags"] = [t.strip() for t in raw_tags.split(",") if t.strip()]
            continue

        # Expected result line (within a test block)
        if current_test and re.match(r'^expected\s*(result)?\s*:', stripped, re.IGNORECASE):
            current_test["expected"] = stripped.split(":", 1)[1].strip()
            continue

        # Numbered step line (1. ... or 1) ...)
        if current_test and re.match(r'^\d+[\.\)]\s+', stripped):
            current_test["steps"].append(stripped)
            continue

        # Plain text inside a test block (treat as a step)
        if current_test and stripped:
            current_test["steps"].append(stripped)

    # Don't forget the last test
    if current_test:
        tests.append(current_test)

    # Auto-detect suite from path if not in file
    if not suite:
        suite = detect_suite_from_path(txt_path)

    return {
        "suite": suite,
        "module_name": txt_path.stem,
        "tests": tests,
    }


def build_module_description(parsed: dict) -> str:
    """Build a single description string covering all test cases for the AI prompt."""
    lines = [f"Generate a complete pytest test MODULE named test_ai_{parsed['module_name']}.py"]
    lines.append(f"The module should contain {len(parsed['tests'])} test function(s), numbered test_01_, test_02_, etc.")
    lines.append("")

    for i, test in enumerate(parsed["tests"], start=1):
        lines.append(f"--- Test {i}: {test['name']} ---")
        if test.get("tags"):
            marks = " ".join(f"@pytest.mark.{t}" for t in test["tags"])
            lines.append(f"Pytest markers: {marks}")
        lines.append("Steps:")
        for step in test["steps"]:
            lines.append(f"  {step}")
        if test["expected"]:
            lines.append(f"Expected Result: {test['expected']}")
        lines.append("")

    return "\n".join(lines)


def find_all_txt_files() -> list[Path]:
    """Find all .txt files across all ai_testcases/ folders in every suite."""
    txt_files = []
    for suite_name, suite_path in SUITES.items():
        ai_dir = suite_path / "ai_testcases"
        if ai_dir.exists():
            txt_files.extend(
                f for f in ai_dir.glob("*.txt")
                if f.name != "example_testcase.txt"   # skip the template
            )
    return sorted(txt_files)


def output_path_for(txt_path: Path, suite_path: Path) -> Path:
    """Determine the output .py path in the suite's test_cases/ folder."""
    for subdir in ["test_cases", "testCases"]:
        tests_dir = suite_path / subdir
        if tests_dir.exists():
            return tests_dir / f"test_ai_{txt_path.stem}.py"
    # Fallback: same folder as txt
    return txt_path.parent / f"test_ai_{txt_path.stem}.py"


def process_file(txt_path: Path, dry_run: bool = False, force: bool = False) -> bool:
    """Process a single txt file → generate a test module. Returns True if generated."""
    parsed = parse_txt_file(txt_path)

    if not parsed["suite"]:
        print(f"[SKIP] {txt_path.name} — could not detect suite. Add 'Suite: <name>' to the file.")
        return False

    if not parsed["tests"]:
        print(f"[SKIP] {txt_path.name} — no test cases found. Use 'Test 1: <name>' to define tests.")
        return False

    suite_name = parsed["suite"]
    if suite_name not in SUITES:
        print(f"[SKIP] {txt_path.name} — unknown suite '{suite_name}'. Available: {', '.join(list_suites())}")
        return False

    suite_path = SUITES[suite_name]
    out_path = output_path_for(txt_path, suite_path)

    if out_path.exists() and not force:
        print(f"[SKIP] {txt_path.name} — {out_path.name} already exists. Use --force to regenerate.")
        return False

    print(f"\n[GENERATE] {txt_path.name} -> {out_path.relative_to(ROOT)}")
    print(f"  Suite      : {suite_name}")
    print(f"  Test cases : {len(parsed['tests'])}")
    for i, t in enumerate(parsed["tests"], 1):
        print(f"    {i}. {t['name']}")

    description = build_module_description(parsed)

    code = generate_test_code(
        description=description,
        suite_name=suite_name,
        output_filename=str(out_path.relative_to(ROOT)),
    )

    # Strip accidental markdown fences
    if code.startswith("```"):
        lines = code.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        code = "\n".join(lines)

    if dry_run:
        print(f"\n--- DRY RUN: would write to {out_path.relative_to(ROOT)} ---")
        print(code)
        print("--- END ---")
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(code, encoding="utf-8")
        print(f"[SUCCESS] Written: {out_path.relative_to(ROOT)}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Process ai_testcases/*.txt files and generate pytest test modules.",
    )
    parser.add_argument("--file", "-f", help="Process a specific .txt file only", default=None)
    parser.add_argument("--suite", "-s", help="Process only txt files for a specific suite", default=None)
    parser.add_argument("--dry-run", action="store_true", help="Print generated code without writing files")
    parser.add_argument("--force", action="store_true", help="Regenerate even if .py already exists")
    args = parser.parse_args()

    _load_env_file()

    if args.file:
        txt_path = Path(args.file)
        if not txt_path.is_absolute():
            txt_path = ROOT / txt_path
        if not txt_path.exists():
            print(f"[ERROR] File not found: {txt_path}")
            sys.exit(1)
        process_file(txt_path, dry_run=args.dry_run, force=args.force)
        return

    txt_files = find_all_txt_files()

    if args.suite:
        suite_path = SUITES.get(args.suite)
        if not suite_path:
            print(f"[ERROR] Unknown suite '{args.suite}'")
            sys.exit(1)
        txt_files = [f for f in txt_files if suite_path in f.parents]

    if not txt_files:
        print("[INFO] No txt files found in any ai_testcases/ folder.")
        print("       Create a .txt file using the format in ai_test_generator/TESTCASE_TEMPLATE.txt")
        return

    print(f"[INFO] Found {len(txt_files)} test case file(s) to process")
    generated = 0
    for txt_path in txt_files:
        if process_file(txt_path, dry_run=args.dry_run, force=args.force):
            generated += 1

    print(f"\n[DONE] Generated {generated} test module(s).")


if __name__ == "__main__":
    main()