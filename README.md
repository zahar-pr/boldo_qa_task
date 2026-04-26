<div align="center">

# 🎭 Plane.so — End-to-End Automation Suite

**Production-grade regression testing for the open-source SaaS Plane**
*Python · Playwright · Allure · GitHub Actions*

[![Allure Report](https://img.shields.io/badge/Allure-Report-blue?logo=qmeta&logoColor=white)](https://zahar-pr.github.io/boldo_qa_task/)
[![Python](https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.49-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![Tests](https://img.shields.io/badge/tests-30%20passed-success)](https://zahar-pr.github.io/boldo_qa_task/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](./LICENSE)

📊 **Live dashboard:** 

</div>

---

![Allure dashboard overview](https://cdn.phototourl.com/free/2026-04-26-046b8b4c-de5d-4f18-884b-3cd9eb187ad3.png)
![Allure test details](https://cdn.phototourl.com/free/2026-04-26-a9eb16ef-de16-4d68-9acb-9e72c63cf93c.png)

## 📌 About the project

A complete End-to-End test suite for [Plane.so](https://app.plane.so) — an open-source project management platform (alternative to Jira / Linear / ClickUp). The coverage is built around critical user journeys: authentication, workspace management, projects, work items, cycles and documentation pages.

The suite is engineered for production use: stable runs in CI, an interactive report with trend history, debug artifacts on failure, and automatic screenshots on errors.

---

## 🎯 Coverage by module

| Module | Tests | Coverage | Severity |
|---|:---:|:---:|---|
| **Authentication** | 5 | ✅ 100% | critical, normal |
| **Workspace** | 3 | ✅ 100% | critical, normal |
| **Projects** | 4 | ✅ 100% | critical, normal |
| **Issues / Work Items** | 6 | ✅ 100% | critical, normal |
| **Views (Kanban / List)** | 3 | ✅ 100% | critical, normal |
| **Cycles / Sprints** | 2 | ✅ 100% | normal |
| **Pages / Documents** | 2 | ✅ 100% | normal |
| **Total** | **25** | ✅ **100%** | |

Plus **6 infrastructure tests** (config, logger, page-object instantiation, auth fixture verification).

📊 Full pass-rate, severity distribution and timeline — on the [Allure dashboard](https://zahar-pr.github.io/boldo_qa_task/).

---

## 🛠️ Tech stack

| Component | Technology | Purpose |
|---|---|---|
| Language | **Python 3.10+** | Test code, fixtures, helpers |
| Browser engine | **Playwright** | Chromium / Firefox / WebKit automation |
| Framework | **pytest** + `pytest-playwright` | Test runner, markers, fixtures |
| Architecture | **Page Object Model** | Decouples selectors from tests |
| Reporting | **Allure 2.30** | Interactive dashboard with trends |
| CI/CD | **GitHub Actions** | Runs on push / PR / daily cron |
| Report hosting | **GitHub Pages** | Public live dashboard |
| Logging | Custom `StepLogger` | STEP / ASSERT / ERROR levels with timestamps |
| Configuration | **pydantic-settings** | Env validation, fail-fast on startup |
| Test data | **Faker** | Unique entities prefixed with `autotest_` |

---

## 🏗️ Architecture

```
boldo_qa_task/
├── conftest.py                          # Global fixtures
├── pytest.ini                           # Markers, allure config
├── requirements-dev.txt                 # Pinned dependency versions
│
├── src/
│   ├── pages/                           # Page Object Model
│   │   ├── base_page.py                 #   Base class with shared methods
│   │   ├── login_page.py                #   Email + OTP form
│   │   ├── workspace_page.py            #   Sidebar, user menu, logout
│   │   ├── project_page.py              #   Project CRUD
│   │   ├── issue_page.py                #   Work item create / edit
│   │   ├── kanban_page.py               #   Kanban board
│   │   ├── list_view_page.py            #   List view
│   │   ├── cycle_page.py                #   Cycles / sprints
│   │   └── page_editor_page.py          #   Wiki pages
│   ├── helpers/
│   │   ├── config.py                    # pydantic-settings + .env
│   │   ├── logger.py                    # StepLogger (STEP / ASSERT / ERROR)
│   │   ├── allure_utils.py              # Screenshots, HTML snapshots
│   │   ├── test_data.py                 # Faker-based data factories
│   │   └── api_client.py                # API client for setup / teardown
│   └── fixtures/                        # Domain-specific fixtures
│
├── tests/
│   ├── auth/                            # TC-001..TC-005
│   ├── workspace/                       # TC-006..TC-008
│   ├── project/                         # TC-009..TC-012
│   ├── issues/                          # TC-013..TC-018
│   ├── views/                           # TC-019..TC-021
│   ├── cycles/                          # TC-022..TC-023
│   └── pages/                           # TC-024..TC-025
│
├── scripts/
│   └── save_auth_state.py               # One-time session saver
│
├── docs/
│   └── SAMPLE_REPORT.md                 # Client-facing report template
│
└── .github/workflows/
    ├── tests.yml                        # E2E suite on push / PR / cron
    └── allure-deploy.yml                # Deploys report to GitHub Pages
```

---

## ⚙️ Key engineering decisions

### 1. Page Object Model with a fluent API

All selectors are encapsulated as `@property` on page classes. Tests read like a scenario:

```python
LoginPage(page, log).submit_email("user@example.com").assert_otp_screen_visible()
```

`@property` rebuilds the locator on every access — eliminates flakiness on SPAs with a dynamic DOM.

### 2. Selector strategy

Priority order: `get_by_role()` → `id` / `name` → `get_by_text()`. **No** hashed Tailwind / CSS-in-JS classes — they change on every UI deploy.

### 3. Authentication via storage_state

Plane uses passwordless auth (OTP via email). The session is saved **once** and reused via `storage_state.json` across every test. Saves ~15 seconds per run.

### 4. Custom logger with STEP / ASSERT / ERROR levels

Every action and assertion is logged in human-readable format with timestamps:

```
[2026-04-26 14:32:01] [INFO]   Test started: tc009_create_project_form_works
[2026-04-26 14:32:02] [STEP]   Click 'Add Project'
[2026-04-26 14:32:03] [ASSERT] Create project modal is visible -- PASSED
[2026-04-26 14:32:05] [STEP]   Fill project name: autotest_project_a3f4b8d2
[2026-04-26 14:32:06] [ASSERT] Create button enabled with valid data -- PASSED
[2026-04-26 14:32:06] [INFO]   Test finished: tc009_create_project_form_works
```

Logs are attached to the Allure report automatically.

### 5. Auto-capture on failure

The `pytest_runtest_makereport` hook fires on every failed test → attaches a screenshot + HTML snapshot to Allure. Debugging a failure takes 30 seconds instead of an hour.

### 6. Test data isolation

Every entity is created with the `autotest_` prefix + uuid suffix (`autotest_project_a3f4b8d2`). Guarantees uniqueness across runs and prevents mixing real and test data.

### 7. CI/CD pipeline

- **Triggers**: push to main, PR, daily cron, manual dispatch
- **Browser matrix**: Chromium (extensible to Firefox / WebKit)
- **Artifacts**: Allure results + Playwright traces (30 / 7-day retention)
- **Auth in CI**: storage_state stored as a base64 GitHub Secret
- **Allure deploy**: automatic publishing to GitHub Pages with trend history

### 8. Allure annotations

Every test is annotated:

```python
@allure.epic("Plane SaaS")
@allure.feature("Authentication")
@allure.story("Login with valid email redirects to OTP screen")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.auth
@pytest.mark.critical
```

This enables filtering by severity / tags / features in the dashboard.

---

## 🚀 Quick start

### Requirements

- Python 3.10+
- Linux / macOS / Windows
- A registered account on [app.plane.so](https://app.plane.so)

### Installation

```bash
git clone https://github.com/zahar-pr/boldo_qa_task.git
cd boldo_qa_task

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements-dev.txt
playwright install --with-deps chromium

cp .env.example .env
# Edit .env: set PLANE_EMAIL and PLANE_WORKSPACE_SLUG

# One-time session save (opens a browser for OTP login)
python scripts/save_auth_state.py
```

### Running the tests

```bash
# All tests
pytest

# Smoke suite (fast critical tests)
pytest -m "smoke and not serial"

# By feature
pytest tests/auth/ -v
pytest tests/project/ -v

# By severity
pytest -m critical -v

# With a different browser
pytest --browser firefox
pytest --browser webkit
```

### Viewing the report locally

```bash
# Run the tests — results appear in allure-results/
pytest

# Local server with the report (requires Java + Allure CLI)
allure serve allure-results
```

---

## 📊 Sample output

```
======================== test session starts =========================
collected 31 items / 1 deselected / 30 selected

tests/auth/test_auth.py::TestAuth::test_tc001_login_redirects_to_otp[chromium] PASSED        [  3%]
tests/auth/test_auth.py::TestAuth::test_tc002_malformed_email_blocks_submit[chromium] PASSED [  6%]
tests/auth/test_auth.py::TestAuth::test_tc003_empty_email_disables_continue[chromium] PASSED [ 10%]
...
tests/workspace/test_workspace.py::TestWorkspace::test_tc008_workspace_settings_accessible[chromium] PASSED [100%]

================== 30 passed, 1 deselected in 187s ===================
```

---

## 📑 Client-facing documentation

Sample test result report: [`docs/SAMPLE_REPORT.md`](./docs/SAMPLE_REPORT.md)

Includes:

- Executive summary (passed / failed / blocked)
- Coverage per module
- Discovered bugs with severity
- Link to the live Allure dashboard
- Recommendations for fix prioritization

---

## 🔧 Extending the suite

### Add a new test

1. Page Object: add a `@property` for the new selector in an existing or new class under `src/pages/`
2. Test: create `test_*.py` under the matching folder `tests/<feature>/`
3. Markers: `@allure.feature(...)`, `@allure.story(...)`, `@pytest.mark.<feature>`
4. Run: `pytest tests/<feature>/ -v`

### Add a new browser to the CI matrix

In `.github/workflows/tests.yml`:

```yaml
strategy:
  matrix:
    browser: [chromium, firefox, webkit]
```

### Refresh storage_state

Plane sessions live ~7 days. When CI starts failing on auth:

```bash
python scripts/save_auth_state.py
base64 -w 0 auth/storage_state.json
# Copy the output into the STORAGE_STATE_B64 GitHub Secret
```
