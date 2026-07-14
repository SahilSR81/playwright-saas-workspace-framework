# Contributing to Playwright SaaS Workspace Framework

Thanks for considering a contribution. This document covers the setup, conventions, and submission process.

## Development Setup

```bash
# Fork and clone
git clone https://github.com/<your-username>/playwright-saas-workspace-framework.git
cd playwright-saas-workspace-framework

# Virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install --with-deps chromium

# Run the suite to confirm everything works
pytest
```

## Project Conventions

### Page Object Model

- All page objects live in `pages/`.
- Locators belong in page classes, not in test files.
- Each page class inherits from `BasePage` and encapsulates locators and actions for a single application view.
- Page methods should return `self` for chaining where appropriate.

### Test Files

- UI tests go in `tests/ui/`.
- BDD step definitions go in `tests/bdd/steps/`.
- Test files are named `test_<feature>.py`.
- Every test function must have at least one marker (`smoke`, `regression`, `api`, `integration`).

### Test Data

- Avoid hardcoding data that depends on shared demo-instance state.
- Use the `config/settings.py` environment-based configuration for credentials and URLs.
- When a test creates data (e.g., an employee record), the test should either clean up after itself or use data that does not conflict with other parallel runs.

### API Tests

- API client classes live in `api/`.
- API tests use the `auth_storage_state` fixture directly to obtain cookies without a browser.

### BDD

- Feature files go in `features/`.
- Step definitions go in `tests/bdd/steps/`.
- Run BDD tests with `pytest tests/bdd/`.

## Commit Messages

Use clear, descriptive commit messages. The team follows a loose Conventional Commits style:

```
type(scope): short summary

- Detail one
- Detail two
```

Common types: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`.

Examples:
- `feat(pim): add employee search by ID test`
- `fix(auth): handle expired storage state in CI`
- `docs(readme): update running tests section`

## Pull Request Process

1. Create a feature branch from `main`.
2. Make your changes following the conventions above.
3. Run the full test suite locally and confirm all tests pass.
4. Ensure every new test has the appropriate marker.
5. Push your branch and open a pull request against `main`.
6. Fill out the pull request template completely.
7. Wait for CI to pass and request a review.

Do not merge your own pull request.

## Reporting Issues

Use the GitHub issue templates for bug reports and feature requests. Include:

- Reproduction steps
- Affected test file and marker
- Relevant logs or screenshots
- Your environment details (OS, Python version, browser)

## Questions

Open a discussion or reach out to [@SahilSR81](https://github.com/SahilSR81).
