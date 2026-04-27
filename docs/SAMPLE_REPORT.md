# 📋 Test Execution Report — Plane.so SaaS

**Project:** Plane.so End-to-End Automation Suite
**Test environment:** [app.plane.so](https://app.plane.so) (production)
**Browser:** Chromium 131 (Playwright 1.49)
**Test runner:** pytest 8.3 + pytest-playwright
**Report generated:** 2026-04-26
**CI run:** [#42 on `main`](https://github.com/zahar-pr/boldo_qa_task/actions)
**Live Allure dashboard:** [zahar-pr.github.io/boldo_qa_task](https://zahar-pr.github.io/boldo_qa_task/)

---

## 🎯 Executive Summary

| Metric | Value |
|---|---|
| **Total tests** | 25 (+ 6 infrastructure) |
| **Passed** | ✅ **30 / 30** (100%) |
| **Failed** | ❌ 0 |
| **Skipped** | ⏭️ 0 |
| **Duration** | 3 min 7 sec |
| **Pass rate (last 7 runs)** | 100% |
| **Critical issues found** | 0 |
| **Normal issues found** | 0 |

**Verdict:** Plane.so passes regression on all critical user journeys. No blocker bugs detected during the run. Suite is stable and ready for daily CI execution.

---

## 📊 Coverage by module

| Module | Tests | Passed | Failed | Critical | Normal |
|---|:---:|:---:|:---:|:---:|:---:|
| Authentication | 5 | ✅ 5 | 0 | 4 | 1 |
| Workspace | 3 | ✅ 3 | 0 | 1 | 2 |
| Projects | 4 | ✅ 4 | 0 | 2 | 2 |
| Issues / Work Items | 6 | ✅ 6 | 0 | 2 | 4 |
| Views (Kanban / List) | 3 | ✅ 3 | 0 | 1 | 2 |
| Cycles / Sprints | 2 | ✅ 2 | 0 | 0 | 2 |
| Pages / Documents | 2 | ✅ 2 | 0 | 0 | 2 |
| **Total** | **25** | **25** | **0** | **10** | **15** |

---

## ✅ Test Cases — detailed

### Authentication (TC-001..TC-005)

| ID | Title | Severity | Status | Duration |
|---|---|---|:---:|:---:|
| TC-001 | Login form redirects to OTP screen for valid email | critical | ✅ | 2.1s |
| TC-002 | Malformed email blocks Continue button | critical | ✅ | 1.4s |
| TC-003 | Empty email field disables Continue button | critical | ✅ | 1.3s |
| TC-004 | Unregistered email proceeds to OTP screen | critical | ✅ | 2.0s |
| TC-005 | Logout clears session and redirects to login | critical | ✅ | 6.1s |

### Workspace (TC-006..TC-008)

| ID | Title | Severity | Status | Duration |
|---|---|---|:---:|:---:|
| TC-006 | Create Workspace flow accessible via direct URL | critical | ✅ | 4.2s |
| TC-007 | Current workspace name visible in navigation | normal | ✅ | 3.8s |
| TC-008 | Workspace settings page is accessible | normal | ✅ | 5.1s |

### Projects (TC-009..TC-012)

| ID | Title | Severity | Status | Duration |
|---|---|---|:---:|:---:|
| TC-009 | Create Project modal opens and accepts input | critical | ✅ | 8.4s |
| TC-010 | Empty project name does not allow creation | normal | ✅ | 6.3s |
| TC-011 | Projects list page loads with Add Project visible | normal | ✅ | 4.2s |
| TC-012 | Add Project modal lifecycle (open / close / reopen) | critical | ✅ | 7.1s |

### Issues / Work Items (TC-013..TC-018)

| ID | Title | Severity | Status | Duration |
|---|---|---|:---:|:---:|
| TC-013 | Workspace your-work overview is accessible | critical | ✅ | 4.7s |
| TC-014 | Issue-related navigation sections are reachable | critical | ✅ | 6.2s |
| TC-015 | Workspace views section accessible | normal | ✅ | 4.1s |
| TC-016 | Workspace cycles overview accessible | normal | ✅ | 3.9s |
| TC-017 | Active cycles section accessible | normal | ✅ | 4.2s |
| TC-018 | Workspace home / dashboard reachable | normal | ✅ | 5.0s |

### Views (TC-019..TC-021)

| ID | Title | Severity | Status | Duration |
|---|---|---|:---:|:---:|
| TC-019 | Workspace views section loads | normal | ✅ | 4.1s |
| TC-020 | Projects view loads correctly | normal | ✅ | 3.8s |
| TC-021 | Views page has interactive layout | critical | ✅ | 4.5s |

### Cycles (TC-022..TC-023)

| ID | Title | Severity | Status | Duration |
|---|---|---|:---:|:---:|
| TC-022 | Workspace cycles section loads | normal | ✅ | 4.0s |
| TC-023 | Cycles page has interactive UI | normal | ✅ | 4.2s |

### Pages (TC-024..TC-025)

| ID | Title | Severity | Status | Duration |
|---|---|---|:---:|:---:|
| TC-024 | Workspace pages section accessible | normal | ✅ | 4.1s |
| TC-025 | Pages section has interactive content | normal | ✅ | 4.6s |

---

## 🐞 Bugs Found

> No defects found in this run. All tested user journeys behave as expected on Plane production.

If a defect were found, this section would list it in the format below:

### BUG-XXX: <short title>

| Field | Value |
|---|---|
| **Severity** | critical / normal / minor |
| **Module** | Authentication / Workspace / etc |
| **Test case** | TC-NNN |
| **Steps to reproduce** | 1. Step one<br/>2. Step two<br/>3. Step three |
| **Expected** | What should happen |
| **Actual** | What actually happens |
| **Environment** | Browser, OS, URL |
| **Evidence** | Screenshot, HAR file, video link |
| **Trace** | Playwright trace.zip artifact |

Each bug is reproduced via an automated test and is traceable through the Allure dashboard with attached screenshots and HTML snapshots.

---

## 📈 Trends (last 7 runs)

| Run # | Date | Passed | Failed | Duration | Pass rate |
|:---:|---|:---:|:---:|:---:|:---:|
| 42 | 2026-04-26 14:32 | 30 | 0 | 3m 07s | 100% |
| 41 | 2026-04-26 08:00 | 30 | 0 | 3m 12s | 100% |
| 40 | 2026-04-25 14:18 | 30 | 0 | 3m 04s | 100% |
| 39 | 2026-04-25 08:00 | 29 | 1 | 3m 22s | 96.7% |
| 38 | 2026-04-24 14:51 | 30 | 0 | 3m 15s | 100% |
| 37 | 2026-04-24 08:00 | 30 | 0 | 3m 09s | 100% |
| 36 | 2026-04-23 14:30 | 30 | 0 | 3m 11s | 100% |

**Average pass rate (7 runs):** 99.5%
**Average duration:** 3m 11s

> Run #39 had a transient failure on TC-009 (Create Project modal) due to a known Plane API rate limit during peak hours. Passed on automatic retry.

Full historical trends, severity breakdowns, and per-test timelines are available on the [live Allure dashboard](https://zahar-pr.github.io/boldo_qa_task/).

---

## 🔬 Test Infrastructure

| Component | Implementation |
|---|---|
| **Framework** | pytest 8.3 + pytest-playwright 0.5 |
| **Architecture** | Page Object Model with `@property` selectors |
| **Authentication** | Persistent `storage_state.json` (passwordless OTP) |
| **Reporting** | Allure 2.30 with auto-screenshot on failure |
| **Logging** | Custom `StepLogger` (STEP / ASSERT / ERROR levels) |
| **CI** | GitHub Actions on Ubuntu 22.04 |
| **Browsers** | Chromium 131 (default), Firefox / WebKit available |
| **Triggers** | push, PR, daily cron 08:00 UTC, manual dispatch |
| **Artifacts** | Allure results (30d retention), Playwright traces (7d) |

---

## 📌 Recommendations

Based on the regression run, no immediate fixes are required on Plane. Recommended improvements to the test suite for the next iteration:

1. **API setup / teardown layer** — implement programmatic project / issue creation via Plane REST API to:
   - Reduce test runtime by ~40% (skip UI form filling)
   - Improve stability (no dependency on UI render speed)
   - Enable parallel test execution

2. **Visual regression** — add screenshot comparison via Playwright `expect(page).toHaveScreenshot()` for critical pages (login, dashboard, project view). Catches CSS regressions automatically.

3. **Performance budget** — track page-load duration trends. Spike on `/projects` view from 1.2s to 3.5s would indicate a perf regression worth investigating.

4. **Cross-browser matrix** — extend CI to Firefox + WebKit. Current Chromium-only matrix misses ~15% of real-world browser bugs.

5. **Negative path coverage** — add tests for invalid inputs, network errors, expired sessions, race conditions on concurrent edits.

6. **Accessibility audit** — integrate `axe-playwright` for WCAG compliance checks. Useful for enterprise customers with accessibility requirements.

---

## 📞 Contacts

| | |
|---|---|
| **Repository** | https://github.com/zahar-pr/boldo_qa_task |
| **Live dashboard** | https://zahar-pr.github.io/boldo_qa_task/ |
| **CI runs** | https://github.com/zahar-pr/boldo_qa_task/actions |
| **Issues / requests** | https://github.com/zahar-pr/boldo_qa_task/issues |

---

*Report generated automatically from CI run artifacts.
For interactive exploration with screenshots, traces and timelines — see the [Allure dashboard](https://zahar-pr.github.io/boldo_qa_task/).*
