# Playwright SaaS Workspace Framework

[![E2E Tests](https://github.com/SahilSR81/playwright-saas-workspace-framework/actions/workflows/e2e-tests.yml/badge.svg)](https://github.com/SahilSR81/playwright-saas-workspace-framework/actions/workflows/e2e-tests.yml)
![Python](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/playwright-1.x-green?logo=playwright&logoColor=white)
![Pytest](https://img.shields.io/badge/pytest-8.x-red?logo=pytest&logoColor=white)
![Docker](https://img.shields.io/badge/docker-24.x-2496ED?logo=docker&logoColor=white)
![Allure](https://img.shields.io/badge/allure-2.x-purple?logo=allure&logoColor=white)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

End-to-end test automation framework for the [OrangeHRM](https://opensource-demo.orangehrmlive.com) open-source HR application. Covers UI validation, API testing, hybrid UI+API flows, and BDD scenarios using Playwright, Pytest, and Allure reporting.

## Key Features

| Feature | Description |
|---------|-------------|
| Page Object Model | Page objects in `pages/` encapsulate locators and interactions for each application view |
| API Layer | Standalone API client classes in `api/` for direct HTTP validation against the application |
| Hybrid Tests | UI + API tests that verify data consistency across the browser and REST interface |
| BDD Support | Gherkin feature files in `features/` with step definitions via pytest-bdd |
| Network Interception | Playwright route mocking and request interception for API stubbing and header injection |
| Parallel Execution | pytest-xdist distributes tests across multiple workers with per-worker storage state isolation |
| CI Retry Resilience | GitHub Actions reruns flaky tests once with a 5-second delay before marking failure |
| Allure Reporting | Rich test reports with environment properties, screenshots, HTML snapshots, traces, and custom failure categorization |
| Docker Support | Containerized test execution for consistent local runs regardless of host environment |
| GitHub Actions CI | Automated pipeline on push/PR to main with artifact upload and 30-day retention |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Browser Automation | Playwright |
| Test Runner | Pytest |
| BDD | pytest-bdd |
| Parallel Execution | pytest-xdist |
| Retry Logic | pytest-rerunfailures |
| Reporting | Allure Report (allure-pytest) |
| Configuration | python-dotenv |
| CI/CD | GitHub Actions |
| Containerization | Docker, Docker Compose |
| Language | Python 3.12 |

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
│   ├── ui/                 # UI and integration tests
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

## Test Markers

| Marker | Description | Defined In |
|--------|-------------|------------|
| `smoke` | Quick sanity checks for critical paths | `pytest.ini`, `conftest.py` |
| `regression` | Full regression test suite | `pytest.ini`, `conftest.py` |
| `api` | API-only tests | `pytest.ini`, `conftest.py` |
| `integration` | UI + API hybrid tests | `pytest.ini`, `conftest.py` |

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

## CI/CD Pipeline

The GitHub Actions workflow at `.github/workflows/e2e-tests.yml` runs on every push and pull request to `main`:

1. Checks out the repository
2. Sets up Python 3.12 with pip caching
3. Installs project dependencies
4. Installs Playwright with Chromium
5. Runs the full test suite with `--reruns 1 --reruns-delay 5` for flaky-test resilience
6. Uploads Allure results as artifacts (30-day retention)

Documentation-only changes (`**/*.md`, `.gitignore`) do not trigger the pipeline.

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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, coding conventions, and pull request guidelines.

## Code of Conduct

This project follows the [Contributor Covenant v2.1](CODE_OF_CONDUCT.md).

## Security

See [SECURITY.md](SECURITY.md) for reporting guidelines.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

**Sahil Singh** -- [@SahilSR81](https://github.com/SahilSR81)
