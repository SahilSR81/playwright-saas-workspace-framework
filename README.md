## 🚧 Project Status  ![Status](https://img.shields.io/badge/status-in%20development-yellow)

Under Active Development

This repository contains an enterprise-focused test automation framework being built using:

- Playwright
- Pytest
- Pytest-BDD
- Requests
- Allure Reporting
- Docker
- GitHub Actions

## Current Progress

- [x] Repository setup
- [x] Framework structure
- [x] Dependency management
- [ ] Authentication module
- [ ] Storage state management
- [ ] API data seeding
- [ ] Network interception
- [ ] BDD integration
- [ ] Docker support
- [ ] CI/CD pipeline

## Planned Features

- UI + API hybrid testing
- Parallel execution
- Session persistence
- Network mocking
- Trace Viewer integration
- Allure reporting
- Containerized execution

Project Update
2026-06-26

During the initial development phase, the framework targeted the OpenProject public demo environment. The demo endpoint later became unavailable, making it unsuitable for long-term automated testing.

To ensure framework stability and continuous development, the System Under Test (SUT) has been migrated to the OrangeHRM public demo application.

This migration only changes the target application. The framework architecture, including the Page Object Model, Pytest integration, Allure reporting, environment-based configuration, and future roadmap, remains unchanged.

The framework is designed to be application-agnostic, allowing future migration to other enterprise web applications with minimal changes to page objects.

More updates coming soon.