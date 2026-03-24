"""
process_testcases.py
====================
Scans all ai_testcases/ folders across every test suite, finds unprocessed
.txt files, and generates a pytest test file for each one.

A .txt file is considered "processed" once a matching .py file exists next to it.

TXT file format (save in <Suite>/ai_testcases/<test_name>.txt):
----------------------------------------------------------------
Test Name: <human readable name>
Suite: <suite name>            ← optional, auto-detected from folder path

Steps:
1. Login as user-1
2. Open the Music App
3. Search for a case by song name using text input
4. Select the case and continue
5. Submit the Play Song form

Expected Result: Form submits successfully and returns to the app home screen
----------------------------------------------------------------

Usage:
    # Process all pending txt files across all suites
    python ai_test_generator/process_testcases.py

    # Process a specific txt file
    python ai_test_generator/process_testcases.py --file Features/CaseSearch/ai_testcases/search_by_song.txt

    # Dry run - show what would be generated without writing files
    python ai_test_generator/process_testcases.py --dry-run

    # Force regenerate even if .py already exists
    python ai_test_generator/process_testcases.py --force
"""

import argparse
import os
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
    Parse a test case .txt file and return:
    {
        "test_name": str,
        "suite": str,
        "steps": str,        # full description to pass to AI
        "expected": str,
    }
    """
    content = txt_path.read_text(encoding="utf-8", errors="ignore").strip()
    lines = content.splitlines()

    test_name = txt_path.stem.replace("_", " ").replace("-", " ").title()
    suite = None
    steps_lines = []
    expected = ""
    in_steps = False

    for line in lines:
        stripped = line.strip()

        if stripped.lower().startswith("test name:"):
            test_name = stripped.split(":", 1)[1].strip()
        elif stripped.lower().startswith("suite:"):
            suite = stripped.split(":", 1)[1].strip()
        elif stripped.lower().startswith("steps:") or stripped.lower() == "steps":
            in_steps = True
        elif stripped.lower().startswith("expected result:") or stripped.lower().startswith("expected:"):
            in_steps = False
            expected = stripped.split(":", 1)[1].strip()
        elif in_steps and stripped:
            steps_lines.append(stripped)
        elif not in_steps and not suite and not stripped.lower().startswith("test name:") and stripped:
            # Lines before "Steps:" header are also part of the description
            steps_lines.append(stripped)

    # Auto-detect suite from path if not specified in file
    if not suite:
        suite = detect_suite_from_path(txt_path)

    # Build a natural language description from steps
    description = f"{test_name}.\n\nSteps:\n" + "\n".join(steps_lines)
    if expected:
        description += f"\n\nExpected Result: {expected}"

    return {
        "test_name": test_name,
        "suite": suite,
        "steps": description,
        "expected": expected,
    }


def find_all_txt_files() -> list[Path]:
    """Find all .txt files across all ai_testcases/ folders in every suite."""
    txt_files = []
    for suite_name, suite_path in SUITES.items():
        ai_dir = suite_path / "ai_testcases"
        if ai_dir.exists():
            txt_files.extend(ai_dir.glob("*.txt"))
    return sorted(txt_files)


def output_path_for(txt_path: Path, suite_path: Path) -> Path:
    """Determine where to write the generated .py file."""
    # Look for test_cases or testCases directory in the suite
    for subdir in ["test_cases", "testCases"]:
        tests_dir = suite_path / subdir
        if tests_dir.exists():
            return tests_dir / f"test_ai_{txt_path.stem}.py"
    # Fallback: write next to the txt file
    return txt_path.parent / f"test_ai_{txt_path.stem}.py"


def process_file(txt_path: Path, dry_run: bool = False, force: bool = False) -> bool:
    """
    Process a single txt file. Returns True if a test was generated.
    """
    parsed = parse_txt_file(txt_path)

    if not parsed["suite"]:
        print(f"[SKIP] {txt_path.name} — could not detect suite. Add 'Suite: <name>' to the file.")
        return False

    suite_name = parsed["suite"]
    if suite_name not in SUITES:
        print(f"[SKIP] {txt_path.name} — unknown suite '{suite_name}'. Available: {', '.join(list_suites())}")
        return False

    suite_path = SUITES[suite_name]
    out_path = output_path_for(txt_path, suite_path)

    if out_path.exists() and not force:
        print(f"[SKIP] {txt_path.name} — already generated ({out_path.name}). Use --force to regenerate.")
        return False

    print(f"\n[GENERATE] {txt_path.name} → {out_path.relative_to(ROOT)}")
    print(f"  Suite      : {suite_name}")
    print(f"  Test Name  : {parsed['test_name']}")

    code = generate_test_code(
        description=parsed["steps"],
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
        description="Process ai_testcases/*.txt files and generate pytest test files.",
    )
    parser.add_argument(
        "--file", "-f",
        help="Process a specific .txt file only",
        default=None,
    )
    parser.add_argument(
        "--suite", "-s",
        help="Process only txt files for a specific suite",
        default=None,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated code without writing files",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate even if .py already exists",
    )
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

    # Scan all suites
    txt_files = find_all_txt_files()

    if args.suite:
        suite_path = SUITES.get(args.suite)
        if not suite_path:
            print(f"[ERROR] Unknown suite '{args.suite}'")
            sys.exit(1)
        txt_files = [f for f in txt_files if suite_path in f.parents]

    if not txt_files:
        print("[INFO] No .txt files found in any ai_testcases/ folder.")
        print("       Create a .txt file in <SuiteFolder>/ai_testcases/ to get started.")
        return

    print(f"[INFO] Found {len(txt_files)} test case file(s)")
    generated = 0
    for txt_path in txt_files:
        if process_file(txt_path, dry_run=args.dry_run, force=args.force):
            generated += 1

    print(f"\n[DONE] Generated {generated} test file(s).")


if __name__ == "__main__":
    main()