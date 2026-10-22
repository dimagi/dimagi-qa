# AI Test Generator — FAQ

---

### What does the AI agent actually do?

It generates a ready-to-run pytest test file (`.py`) from plain English steps written in a `.txt` file.
It does **not** run the tests. Your existing GitHub Actions workflows handle test execution on their normal schedule.

---

### How does the agent know which function to call?

The agent scans all `testPages/` files in your suite using Python's AST parser and extracts every class name and method signature. That full list is sent to the AI along with your description. The AI then matches your plain English steps to the closest matching method.

For example, when you write:
```
3. Open the Worker Activity report
```
The scanner has already told the AI that `ReportPage` has a method called `worker_activity_report()` — so it calls exactly that.

---

### If I add new functionality, do I need to update the agent?

No configuration needed. Once a developer adds a new method to a page object in `testPages/`, the scanner automatically picks it up the next time the agent runs. The agent always reflects the latest state of your page objects.

| Task | Who does it |
|---|---|
| Write page object methods + locators | Developer (in `testPages/`) |
| Write test steps in plain English | Anyone (in `ai_testcases/*.txt`) |
| Generate the test function code | Agent (automatically) |

---

### Can the agent generate page object methods and locators too?

No. The agent cannot see your actual UI or browser, so it cannot generate accurate XPath/CSS locators. Page object methods need to be written by a developer who knows the UI structure.

Once those methods exist in `testPages/`, the agent can use them freely in generated tests.

---

### One txt file or one test per file?

One `.txt` file = one `.py` test module with multiple test functions.

```
HQSmokeTests/ai_testcases/reports.txt     →    HQSmokeTests/testCases/test_ai_reports.py
  Test 1: Verify report sections                  def test_01_verify_report_sections(...)
  Test 2: Run Worker Activity report              def test_02_run_worker_activity_report(...)
  Test 3: Run Case Activity report                def test_03_run_case_activity_report(...)
```

Organise your txt files by feature area — e.g. `reports.txt`, `mobile_workers.txt`, `exports.txt`.

---

### Will the generated test run perfectly straight away?

Mostly yes, but review it first. The agent uses real method names from your page objects, so the structure and logic will be correct. Occasionally, when a specific UI element has no matching method in the page objects, the AI inserts a placeholder like:

```python
page.get_element("locator_for_monitor_workers")
```

A developer needs to replace these placeholders with the real locator from the page object. Everything else should be runnable as-is.

---

### Does it modify my existing test files?

Never. The agent only creates new files named `test_ai_<filename>.py`. Your existing hand-written test files are never touched.

---

### How do I trigger generation locally?

```bash
# Single txt file
python ai_test_generator/process_testcases.py --file HQSmokeTests/ai_testcases/reports.txt

# All txt files across all suites at once
python ai_test_generator/process_testcases.py

# Preview without writing the file
python ai_test_generator/process_testcases.py --file HQSmokeTests/ai_testcases/reports.txt --dry-run

# Regenerate a file that already exists
python ai_test_generator/process_testcases.py --file HQSmokeTests/ai_testcases/reports.txt --force
```

---

### How do I trigger generation from GitHub (no local setup)?

**Option A — Push a txt file (automatic):**
1. Add or edit a `.txt` file in any suite's `ai_testcases/` folder
2. Push/commit to GitHub
3. The **AI Test Generator** workflow triggers automatically
4. The generated `.py` file is committed back to the repo

**Option B — Run manually from GitHub UI:**
1. Go to **Actions** tab on GitHub
2. Select **AI Test Generator** from the left sidebar
3. Click **Run workflow**
4. Choose the suite, type your description, click **Run workflow**

---

### Do I need a different workflow for each test suite?

No. The single `ai-test-generator.yml` workflow handles all 13+ suites. It detects which suite a txt file belongs to automatically from the folder path.

---

### What if I add a new test suite in the future?

A developer needs to add the new suite to the `SUITES` dictionary in `ai_test_generator/scanner.py` and create an `ai_testcases/` folder in the suite directory. After that, it works the same as all other suites.

---

### How much does it cost to generate a test?

Each test generation costs approximately **$0.01–$0.03** using GPT-4o. This only applies when generating — your daily test suite runs (Selenium/pytest) are unaffected and cost nothing extra.

---

### Where is the API key stored?

- **Locally:** `ai_test_generator/.env` — this file is in `.gitignore` and is never committed
- **GitHub Actions:** stored as a repository secret named `OPENAI_API_KEY` (Settings → Secrets and variables → Actions)

---

### What suites are supported?

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
