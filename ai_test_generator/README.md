# AI Test Generator

Automatically generates ready-to-run pytest test files from plain English test descriptions.
Non-technical team members write simple steps in a `.txt` file — the AI writes the code.

---

## How It Works

```
You write a .txt file          →   AI reads it   →   .py test module is created
HQSmokeTests/                       (OpenAI)         HQSmokeTests/
  ai_testcases/                                         testCases/
    reports.txt                                           test_ai_reports.py
      Test 1: ...                                           def test_01_...
      Test 2: ...                                           def test_02_...
```

The generated `.py` file is placed in the suite's existing `testCases/` or `test_cases/` folder
and follows the exact same structure as your hand-written tests — same imports, fixtures,
page objects, and naming conventions.

---

## Quick Start (Local)

### Step 1 — Install the dependency
```bash
pip install openai
```

### Step 2 — Add your OpenAI API key to the `.env` file
Open `ai_test_generator/.env` and set:
```
OPENAI_API_KEY=sk-proj-your-key-here
```

### Step 3 — Write your test cases in a `.txt` file

Go to your suite's `ai_testcases/` folder (e.g. `HQSmokeTests/ai_testcases/`),
copy `example_testcase.txt`, rename it, and fill in your steps:

```
Suite: HQSmokeTests

Test 1: Verify reports module loads all sections
1. Navigate to Reports
2. Click View All
3. Verify Monitor Workers section is displayed
4. Verify Inspect Data section is displayed
Expected Result: All report sections are visible

Test 2: Create a new mobile worker
1. Navigate to Users > Mobile Workers
2. Click Add Mobile Worker
3. Enter a username and password
4. Save the new worker
Expected Result: Worker is created and appears in the list
```

### Step 4 — Run the generator
```bash
# Generate from a specific txt file
python ai_test_generator/process_testcases.py --file HQSmokeTests/ai_testcases/reports.txt

# Generate from ALL txt files across ALL suites at once
python ai_test_generator/process_testcases.py

# Preview without writing the file
python ai_test_generator/process_testcases.py --file HQSmokeTests/ai_testcases/reports.txt --dry-run

# Regenerate an already-generated file
python ai_test_generator/process_testcases.py --file HQSmokeTests/ai_testcases/reports.txt --force
```

### Step 5 — Review and run the generated test
```bash
pytest HQSmokeTests/testCases/test_ai_reports.py -v
```

---

## GitHub Actions (No Local Setup Needed)

Your team members can generate tests directly from GitHub without any local setup.

### Option A — Push a txt file (automatic)
1. Add or edit a `.txt` file in any suite's `ai_testcases/` folder
2. Push/commit to GitHub
3. The **AI Test Generator** workflow triggers automatically
4. The generated `.py` file is committed back to the repo

### Option B — Run manually from GitHub UI
1. Go to **Actions** tab on GitHub
2. Select **AI Test Generator** from the left sidebar
3. Click **Run workflow**
4. Choose the suite, type your test description, click **Run workflow**

---

## Available Suites

| Suite Name | Folder |
|---|---|
| `CaseSearch` | `Features/CaseSearch/` |
| `DataDictionary` | `Features/DataDictionary/` |
| `FindDataById` | `Features/FindDataById/` |
| `Lookuptable` | `Features/Lookuptable/` |
| `MultiSelect` | `Features/MultiSelect/` |
| `PowerBI` | `Features/Powerbi_integration_exports/` |
| `SplitScreenCaseSearch` | `Features/SplitScreenCaseSearch/` |
| `ElasticSearch` | `ElasticSearchTests/` |
| `ExportTests` | `ExportTests/` |
| `Formplayer` | `Formplayer/` |
| `HQSmokeTests` | `HQSmokeTests/` |
| `P1P2Tests` | `P1P2Tests/` |
| `RequestAPI` | `RequestAPI/` |
| `USH_CO_BHA` | `USH_Apps/CO_BHA/` |
| `BHAStressTest` | `QA_Requests/BHAStressTest/` |

---

## txt File Format

```
Suite: <suite name>

Test 1: <short test name>
1. <step one>
2. <step two>
3. <step three>
Expected Result: <what should happen>

Test 2: <short test name>
1. <step one>
2. <step two>
Expected Result: <what should happen>
```

**Rules:**
- `Suite:` line is required (or place the file in the correct `ai_testcases/` folder — it auto-detects)
- Each test block starts with `Test 1:`, `Test 2:`, etc.
- Steps can be numbered (`1.`) or plain bullet points
- `Expected Result:` is optional but recommended
- One `.txt` file → one `.py` test module with multiple test functions

---

## File Structure

```
ai_test_generator/
├── generate_test.py       # Core generator — calls OpenAI API
├── process_testcases.py   # Processes txt files → generates test modules
├── scanner.py             # Scans page objects and user inputs from the framework
├── requirements.txt       # openai>=1.0.0
├── .env                   # Your API key (never committed)
├── .env.example           # Template for the .env file
├── TESTCASE_TEMPLATE.txt  # Blank template to copy into ai_testcases/
└── README.md              # This file

Each suite/
└── ai_testcases/
    ├── example_testcase.txt   # Template showing the format
    └── your_tests.txt         # Your test cases → generates test_ai_your_tests.py
```

---

## Tips

- **Be specific in your steps** — mention usernames, menu names, form names, and field names
  that exist in your application. The AI uses these to pick the right page object methods.
- **One txt file per feature area** — e.g. `reports.txt`, `mobile_workers.txt`, `exports.txt`
- **Review the generated file** before running — the AI may occasionally use a placeholder
  locator if a specific UI element isn't in the existing page objects. Add it manually if needed.
- **The generator never modifies existing test files** — it only creates new `test_ai_*.py` files.