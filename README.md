# Playwright SaaS Workspace Framework

[![E2E Tests](https://github.com/SahilSR81/playwright-saas-workspace-framework/actions/workflows/e2e-tests.yml/badge.svg)](https://github.com/SahilSR81/playwright-saas-workspace-framework/actions/workflows/e2e-tests.yml)
![Python](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/playwright-1.x-green?logo=playwright&logoColor=white)
![Pytest](https://img.shields.io/badge/pytest-8.x-red?logo=pytest&logoColor=white)
![Docker](https://img.shields.io/badge/docker-24.x-2496ED?logo=docker&logoColor=white)
![Allure](https://img.shields.io/badge/allure-2.x-purple?logo=allure&logoColor=white)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

End-to-end test automation framework for the [OrangeHRM](https://opensource-demo.orangehrmlive.com) open-source HR application. Covers UI validation, API testing, hybrid UI+API flows, and BDD scenarios using Playwright, Pytest, and Allure reporting.

---

## Key Features

| Area | What's implemented |
|------|-------------------|
| UI Automation | Page Object Model across Login, Dashboard, Admin, PIM, and Logout modules |
| API Testing | requests-based API layer (BaseAPI, EmployeeAPI) with session/cookie reuse from browser auth |
| Hybrid Tests | Tests that validate the same state through both the UI and the API |
| BDD Support | pytest-bdd feature files (`features/*.feature`) with step definitions |
| Network Interception | Request blocking/mocking helper to simulate broken images, CSS, and server errors |
| Parallel Execution | pytest-xdist with a worker-isolated auth storage state per xdist worker |
| CI Resilience | Automatic retry (pytest-rerunfailures) + `domcontentloaded`-based navigation to handle a shared public demo instance gracefully |
| Reporting | Allure reports with a custom `categories.json` that auto-buckets failures (Locator / Timeout / Assertion / Network / API) |
| Containerized | Fully Dockerized execution via Dockerfile + docker-compose.yml |
| CI/CD | GitHub Actions workflow running on every push/PR to main |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Browser Automation | Playwright (sync API) |
| Test Runner | Pytest |
| BDD | pytest-bdd |
| API Client | requests |
| Parallelization | pytest-xdist |
| CI Resilience | pytest-rerunfailures |
| Reporting | Allure (allure-pytest) |
| Config Management | python-dotenv |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Application Under Test | [OrangeHRM](https://opensource-demo.orangehrmlive.com) (public demo) |

---

## Project Structure

```
playwright-saas-workspace-framework/
├── api/                    # API client classes
│   ├── base_api.py
│   └── employee_api.py
├── config/
│   └── settings.py         # Central configuration from environment variables
├── data/                   # Test data files
├── features/               # BDD feature files
│   ├── admin.feature
│   └── login.feature
├── pages/                  # Page Object Model classes
│   ├── admin_page.py
│   ├── base_page.py
│   ├── dashboard_page.py
│   ├── login_page.py
│   ├── logout_page.py
│   └── pim_page.py
├── scripts/
│   ├── docker-run.sh       # Docker execution helper
│   └── run_parallel.sh     # Parallel execution wrapper
├── tests/
│   ├── ui/                 # UI and integration tests (72 cases)
│   └── bdd/
│       └── steps/          # BDD step definitions
├── utils/                  # Shared helpers
│   ├── allure_helper.py
│   ├── logger.py
│   ├── network_helper.py
│   └── screenshot_helper.py
├── categories.json         # Allure failure categorization buckets
├── conftest.py             # Pytest fixtures, hooks, and auth orchestration
├── Dockerfile
├── docker-compose.yml
├── pytest.ini              # Pytest configuration
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.12
- pip
- Docker (optional, for containerized runs)

### Installation

```bash
# Clone the repository
git clone https://github.com/SahilSR81/playwright-saas-workspace-framework.git
cd playwright-saas-workspace-framework

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install --with-deps chromium
```

You're ready to run tests.

---

## Configuration

All settings are read from environment variables with sensible defaults. Create a `.env` file in the project root for local development (already gitignored).

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `https://opensource-demo.orangehrmlive.com/web/index.php/auth/login` | Application login URL |
| `BROWSER` | `chromium` | Playwright browser engine to use |
| `BROWSERS` | `chromium,firefox,webkit` | Comma-separated list for multi-browser runs |
| `HEADLESS` | `False` | Run browser in headless mode |
| `SLOW_MO` | `0` | Slow-motion delay in milliseconds between actions |
| `TIMEOUT` | `30000` | Default navigation and action timeout in milliseconds |
| `ENV` | `QA` | Environment label displayed in Allure reports |
| `USERNAME` | `Admin` | Login credential username |
| `PASSWORD` | `admin123` | Login credential password |
| `PARALLEL_WORKERS` | `0` | Number of parallel workers (0 = disabled) |

---

## Running Tests

### Sequential

```bash
pytest
```

### Parallel

```bash
# Auto-detect CPU count
pytest -n auto

# Fixed worker count
pytest -n 4
```

### By Marker

```bash
pytest -m smoke
pytest -m regression
pytest -m api
pytest -m integration
```

### Using Scripts

```bash
# Parallel with marker filter
bash scripts/run_parallel.sh auto smoke
bash scripts/run_parallel.sh 4 regression

# Docker execution
bash scripts/docker-run.sh
```

### Docker

```bash
docker compose up --build
```

### BDD

```bash
pytest tests/bdd/
```

---

## Test Markers

| Marker | Description |
|--------|-------------|
| `smoke` | Quick sanity checks for critical paths |
| `regression` | Full regression test suite |
| `api` | API-only tests |
| `integration` | UI + API hybrid tests |

---

## Test Reporting

Generate and view Allure reports locally:

```bash
# Serve the report in a browser
allure serve reports/allure-results

# Generate a static report
allure generate reports/allure-results -o reports/allure-report --clean
```

### Failure Categorization

The `categories.json` file defines custom failure buckets for the Allure report. Failed tests are automatically grouped into:

| Category | Matches |
|----------|---------|
| UI Element Failure | Element not found, unable to locate, not visible/clickable |
| Locator Failure | Strict mode violation, selector errors |
| Assertion Failure | Expected vs actual mismatches |
| Network Failure | Connection errors, HTTP status codes |
| Timeout Failure | Navigation and action timeouts |
| API Failure | API response errors and status codes |

### Automatic Diagnostics

On test failure, the framework automatically attaches to the Allure report:

- Screenshot of the failure state
- Full page HTML
- Current URL
- Browser console logs
- Playwright trace file

---

## CI/CD Pipeline

The GitHub Actions workflow at `.github/workflows/e2e-tests.yml` runs on every push and pull request to `main`:

1. Checks out the repository
2. Sets up Python 3.12 with pip caching
3. Installs project dependencies
4. Installs Playwright with Chromium
5. Runs the full test suite with `--reruns 1 --reruns-delay 5` for flaky-test resilience
6. Uploads Allure results as artifacts (30-day retention)

Documentation-only changes (`**/*.md`, `.gitignore`) do not trigger the pipeline.

---

## Test Coverage

```
72 test cases | 9 modules | 100% passing
```

| Module | Tests | What's Covered |
|--------|------:|----------------|
| Login | 9 | Valid/invalid credentials, empty fields, whitespace, case sensitivity |
| Dashboard | 5 | Page load, URL, side nav, quick launch, widgets (time at work, my actions) |
| Admin | 16 | System Users page, table, search (valid/invalid/special chars/long/rapid), filters, reset, case sensitivity |
| PIM | 19 | Add/edit/delete employees, search by ID, file upload, empty fields, special chars, long names |
| Logout | 5 | Logout option visibility, successful logout, redirect, session invalidation, refresh after logout |
| API (Base) | 4 | Session creation, default headers, base URL, session close |
| API (Employee) | 6 | Endpoint hit, create payload, custom employee ID, employee API object, get all, create employee |
| Network | 6 | Block images, block CSS, mock 500, mock employee API, offline mode, restore network |
| BDD | 2 | Feature files with step definitions (login, admin) |

---

## Troubleshooting

<details>
<summary><strong>Login timeouts against the shared public demo</strong></summary>

The OrangeHRM demo instance is publicly shared and can be slow or temporarily unavailable. The framework includes a `_navigate_with_retry` helper that retries navigation up to 3 times with exponential backoff. If you still hit timeouts:

- Increase the `TIMEOUT` environment variable (e.g., `TIMEOUT=60000`)
- Run tests during off-peak hours
- Check the [OrangeHRM demo status](https://opensource-demo.orangehrmlive.com) before debugging test logic

</details>

<details>
<summary><strong>Employee name-search eventual consistency vs ID search</strong></summary>

After creating an employee via the API, searching by name may return stale results due to the demo app's eventual consistency. Searching by Employee ID is more reliable. If a test fails after employee creation, the name index may need a longer wait or a retry loop.

</details>

<details>
<summary><strong>Responsive table locator differences</strong></summary>

OrangeHRM renders table rows differently depending on viewport width. The framework uses `.oxd-table-card` for wider viewports. If tests fail with table-related locator errors, verify the browser context dimensions match the expected responsive breakpoint.

</details>

<details>
<summary><strong>Tests pass locally but fail in CI</strong></summary>

Since the CI pipeline runs against the same shared public demo instance, data created by other users can cause test failures. Common causes:

- Pre-existing admin or employee records interfering with assertions
- Rate limiting or temporary outages on the demo server
- Different Chromium versions between local and CI environments

The CI pipeline reruns failed tests once to handle transient issues. For persistent failures, add explicit wait-for conditions or relax assertions on shared-state data.

</details>

---

## Author

**Sahil Singh** -- [@SahilSR81](https://github.com/SahilSR81)

---

> *"The measure of a person is how they handle things when they break."*
> -- *Roronoa Zoro, One Piece*
