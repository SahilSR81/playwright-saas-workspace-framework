## Project Status ![Status](https://img.shields.io/badge/status-in%20development-yellow)

Under Active Development

This repository contains an enterprise-grade test automation framework built with:

* Playwright
* Pytest
* Pytest-BDD
* Requests
* Allure Reporting
* Docker
* GitHub Actions

## Current Progress

* ✅ Repository setup
* ✅ Framework structure
* ✅ Dependency management
* ✅ Authentication module
* ✅ Storage state management
* ✅ Dashboard module
* ✅ Navigation module
* ✅ Logout workflow
* ✅ Admin module
* ✅ PIM module
* ✅ API framework
* ✅ Network interception
* ✅ Hybrid API + UI validation
* ✅ Advanced Allure reporting
* ✅ Parallel execution
* ✅ Docker support
* ✅ BDD integration
* ⬜ CI/CD pipeline

## Running Tests

### Sequential (default)

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

### Using Script

```bash
bash scripts/run_parallel.sh auto smoke
bash scripts/run_parallel.sh 4 regression
```

### Docker

```bash
docker compose up --build
```

## Test Markers

| Marker        | Description                          |
|---------------|--------------------------------------|
| `smoke`       | Critical path sanity checks          |
| `regression`  | Full regression suite                |
| `api`         | API-only tests                       |
| `integration` | UI + API hybrid tests                |

---

## Project Update

### 2026-07-12

Integrated Behavior-Driven Development (BDD) using pytest-bdd to support business-readable test scenarios while reusing the existing Page Object Model and Playwright fixtures. This milestone improves collaboration between technical and non-technical stakeholders by expressing automation workflows in Gherkin while preserving a single implementation layer.

### 2026-07-11

Improved authentication resilience across the framework. Added automatic session refresh when storage state expires during test execution, with seamless re-authentication and state syncing between worker-specific and shared storage files. Refined API cookie loading with a fallback mechanism that gracefully handles missing storage state files. Adjusted environment variable loading to respect system-level defaults.

### 2026-07-10

Containerized the automation framework using Docker to provide a consistent execution environment across development machines and CI pipelines. Added Docker configuration for dependency management, browser installation, and automated test execution, simplifying project setup and improving portability.

More updates coming soon...
