"""
scanner.py
Scans all test suites in the dimagi-qa project and extracts:
- Available page object classes and their public methods
- Suite structure (test_pages/, test_cases/, user_inputs/)
- User input classes and their attributes
"""

import ast
import os
from pathlib import Path


ROOT = Path(__file__).parent.parent

# All known test suites mapped to their folder paths
SUITES = {
    "CaseSearch":             ROOT / "Features" / "CaseSearch",
    "DataDictionary":         ROOT / "Features" / "DataDictionary",
    "FindDataById":           ROOT / "Features" / "FindDataById",
    "Lookuptable":            ROOT / "Features" / "Lookuptable",
    "MultiSelect":            ROOT / "Features" / "MultiSelect",
    "PowerBI":                ROOT / "Features" / "Powerbi_integration_exports",
    "SplitScreenCaseSearch":  ROOT / "Features" / "SplitScreenCaseSearch",
    "ElasticSearch":          ROOT / "ElasticSearchTests",
    "ExportTests":            ROOT / "ExportTests",
    "Formplayer":             ROOT / "Formplayer",
    "HQSmokeTests":           ROOT / "HQSmokeTests",
    "P1P2Tests":              ROOT / "P1P2Tests",
    "RequestAPI":             ROOT / "RequestAPI",
    "USH_CO_BHA":             ROOT / "USH_Apps" / "CO_BHA",
    "MobileTest":             ROOT / "MobileTest",
    "BHAStressTest":          ROOT / "QA_Requests" / "BHAStressTest",
}

COMMON_UTILITIES = ROOT / "common_utilities"


def _get_init_signature(node: ast.ClassDef) -> str:
    """Extract the __init__ constructor args (excluding self) for a class."""
    for item in node.body:
        if isinstance(item, ast.FunctionDef) and item.name == "__init__":
            args = [a.arg for a in item.args.args if a.arg != "self"]
            return ", ".join(args)
    return ""


def _extract_classes_and_methods(filepath: Path) -> list[dict]:
    """Parse a Python file and return class info with constructor + public method signatures."""
    try:
        source = filepath.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(source)
    except Exception:
        return []

    results = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue

        init_args = _get_init_signature(node)
        instantiation = f"{node.name}({init_args})"

        methods = []
        for item in node.body:
            if not isinstance(item, ast.FunctionDef):
                continue
            if item.name.startswith("_"):
                continue

            # Build readable signature
            args = [a.arg for a in item.args.args if a.arg != "self"]
            defaults = item.args.defaults
            if defaults:
                num_defaults = len(defaults)
                required = args[:-num_defaults] if num_defaults < len(args) else []
                optional = args[-num_defaults:] if num_defaults <= len(args) else args
                sig_parts = required + [f"{a}=..." for a in optional]
            else:
                sig_parts = args

            # Grab first line of docstring if present
            docstring = ""
            if (item.body and isinstance(item.body[0], ast.Expr)
                    and isinstance(item.body[0].value, ast.Constant)):
                docstring = item.body[0].value.value.strip().splitlines()[0]

            methods.append({
                "name": item.name,
                "signature": f"{item.name}({', '.join(sig_parts)})",
                "doc": docstring,
            })

        if methods:
            results.append({
                "class": node.name,
                "file": str(filepath.relative_to(ROOT)),
                "instantiation": instantiation,   # e.g. "ReportPage(driver)"
                "methods": methods,
            })

    return results


def _extract_constants(filepath: Path) -> dict:
    """Extract top-level string constants and class attributes from a Python file."""
    try:
        source = filepath.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(source)
    except Exception:
        return {}

    constants = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            if isinstance(item.value, ast.Constant):
                                constants[f"{node.name}.{target.id}"] = item.value.s
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if isinstance(node.value, ast.Constant):
                        constants[target.id] = node.value.s
    return constants


def _find_page_files(suite_path: Path) -> list[Path]:
    """Find all page object files in a suite."""
    page_files = []
    for subdir in ["test_pages", "testPages", "pages"]:
        pages_dir = suite_path / subdir
        if pages_dir.exists():
            page_files.extend(pages_dir.rglob("*.py"))
    return page_files


def _find_test_files(suite_path: Path) -> list[Path]:
    """Find existing test files to use as reference examples."""
    test_files = []
    for subdir in ["test_cases", "testCases"]:
        tests_dir = suite_path / subdir
        if tests_dir.exists():
            test_files.extend(
                f for f in tests_dir.glob("test_*.py")
                if "conftest" not in f.name
            )
    return sorted(test_files)


def _find_user_input_files(suite_path: Path) -> list[Path]:
    """Find user input / test data files."""
    input_files = []
    for subdir in ["user_inputs", "userInputs", "UserInputs"]:
        inputs_dir = suite_path / subdir
        if inputs_dir.exists():
            input_files.extend(inputs_dir.rglob("*.py"))
    return input_files


def scan_common_utilities() -> str:
    """Return a summary of BasePage and WebApps methods."""
    lines = []

    base_page = COMMON_UTILITIES / "selenium" / "base_page.py"
    webapps = COMMON_UTILITIES / "selenium" / "webapps.py"
    login_page = COMMON_UTILITIES / "hq_login" / "login_page.py"

    for filepath in [base_page, webapps, login_page]:
        if not filepath.exists():
            continue
        classes = _extract_classes_and_methods(filepath)
        for cls in classes:
            lines.append(f"\nClass: {cls['class']} (from {cls['file']})")
            lines.append(f"  INSTANTIATE AS: {cls['instantiation']}")
            for m in cls["methods"]:
                line = f"  - {m['signature']}"
                if m["doc"]:
                    line += f"  # {m['doc']}"
                lines.append(line)

    return "\n".join(lines)


def scan_suite(suite_name: str) -> dict:
    """
    Scan a specific test suite and return structured context:
    {
      "suite_name": str,
      "suite_path": str,
      "page_classes": [{"class": str, "file": str, "methods": [...]}],
      "user_inputs": {attr: value, ...},
      "test_dirs": {"test_cases": str, "test_pages": str, "user_inputs": str},
      "existing_test_example": str,   # content of first test file
      "conftest_example": str,        # content of conftest.py
    }
    """
    suite_path = SUITES.get(suite_name)
    if not suite_path or not suite_path.exists():
        available = ", ".join(SUITES.keys())
        raise ValueError(
            f"Suite '{suite_name}' not found. Available suites: {available}"
        )

    result = {
        "suite_name": suite_name,
        "suite_path": str(suite_path.relative_to(ROOT)),
        "page_classes": [],
        "user_inputs": {},
        "test_dirs": {},
        "existing_test_example": "",
        "conftest_example": "",
    }

    # Page objects
    for pf in _find_page_files(suite_path):
        result["page_classes"].extend(_extract_classes_and_methods(pf))

    # Directory names
    for subdir in ["test_cases", "testCases"]:
        if (suite_path / subdir).exists():
            result["test_dirs"]["test_cases"] = subdir
            break
    for subdir in ["test_pages", "testPages"]:
        if (suite_path / subdir).exists():
            result["test_dirs"]["test_pages"] = subdir
            break
    for subdir in ["user_inputs", "userInputs", "UserInputs"]:
        if (suite_path / subdir).exists():
            result["test_dirs"]["user_inputs"] = subdir
            break

    # User inputs (constants for test data)
    for uf in _find_user_input_files(suite_path):
        result["user_inputs"].update(_extract_constants(uf))

    # Grab first existing test as reference example (truncated to 100 lines)
    test_files = _find_test_files(suite_path)
    if test_files:
        try:
            lines = test_files[0].read_text(encoding="utf-8", errors="ignore").splitlines()
            result["existing_test_example"] = "\n".join(lines[:100])
        except Exception:
            pass

    # Grab conftest.py
    for subdir in ["test_cases", "testCases"]:
        conftest = suite_path / subdir / "conftest.py"
        if conftest.exists():
            try:
                lines = conftest.read_text(encoding="utf-8", errors="ignore").splitlines()
                result["conftest_example"] = "\n".join(lines[:60])
            except Exception:
                pass
            break

    return result


def list_suites() -> list[str]:
    """Return all available suite names."""
    return [name for name, path in SUITES.items() if path.exists()]


def format_suite_context(suite_data: dict, common_utils: str) -> str:
    """Format suite scan data into a readable context string for the AI prompt."""
    lines = []

    lines.append(f"=== SUITE: {suite_data['suite_name']} ===")
    lines.append(f"Path: {suite_data['suite_path']}")
    lines.append("")

    # Directory structure
    dirs = suite_data["test_dirs"]
    lines.append("Directory layout:")
    lines.append(f"  Tests:       {suite_data['suite_path']}/{dirs.get('test_cases', 'test_cases')}/")
    lines.append(f"  Page objects:{suite_data['suite_path']}/{dirs.get('test_pages', 'test_pages')}/")
    lines.append(f"  User inputs: {suite_data['suite_path']}/{dirs.get('user_inputs', 'user_inputs')}/")
    lines.append("")

    # Common utilities
    lines.append("=== COMMON UTILITIES (available in ALL suites) ===")
    lines.append(common_utils)
    lines.append("")

    # Suite-specific page objects
    if suite_data["page_classes"]:
        lines.append("=== SUITE-SPECIFIC PAGE OBJECTS ===")
        lines.append("IMPORTANT: Instantiate each class EXACTLY as shown — do not add or remove parameters.")
        for cls in suite_data["page_classes"]:
            lines.append(f"\nClass: {cls['class']} (from {cls['file']})")
            lines.append(f"  INSTANTIATE AS: {cls['instantiation']}")
            for m in cls["methods"]:
                line = f"  - {m['signature']}"
                if m["doc"]:
                    line += f"  # {m['doc']}"
                lines.append(line)
    else:
        lines.append("=== NO SUITE-SPECIFIC PAGE OBJECTS FOUND ===")
        lines.append("Use only common_utilities (BasePage, WebApps, LoginPage).")
    lines.append("")

    # User inputs sample
    if suite_data["user_inputs"]:
        lines.append("=== AVAILABLE USER INPUT VALUES (sample) ===")
        for k, v in list(suite_data["user_inputs"].items())[:40]:
            lines.append(f"  {k} = '{v}'")
    lines.append("")

    # Existing test as reference
    if suite_data["existing_test_example"]:
        lines.append("=== EXISTING TEST EXAMPLE (reference only) ===")
        lines.append(suite_data["existing_test_example"])
    lines.append("")

    # Conftest structure
    if suite_data["conftest_example"]:
        lines.append("=== CONFTEST.PY (fixture reference) ===")
        lines.append(suite_data["conftest_example"])

    return "\n".join(lines)


if __name__ == "__main__":
    # Quick smoke test
    print("Available suites:", list_suites())
    print("\nCommon utilities:")
    print(scan_common_utilities()[:500])
    print("\nScanning CaseSearch...")
    data = scan_suite("CaseSearch")
    print(f"Found {len(data['page_classes'])} page classes")
    print(f"Found {len(data['user_inputs'])} user input values")
