# Security Policy

## Scope

This repository is a test automation framework. It tests the public [OrangeHRM](https://opensource-demo.orangehrmlive.com) demo application and does not handle production secrets, user data, or sensitive business information.

The `.env` file contains only public demo credentials (`Admin`/`admin123`) and is gitignored.

## Reporting Framework Vulnerabilities

If you discover a security issue in the framework itself (e.g., insecure handling of credentials, exposed secrets in logs, dependency vulnerabilities), please report it privately:

1. Do not open a public issue.
2. Contact the maintainer via [GitHub](https://github.com/SahilSR81) using the private contact options on the profile page.
3. Include a description of the issue, steps to reproduce, and the potential impact.

You should receive an acknowledgment within 72 hours.

## Out of Scope

- Vulnerabilities in the OrangeHRM application itself. Report those to the [OrangeHRM project](https://github.com/orangehrm/orangehrm).
- Issues related to the shared demo instance being slow, down, or returning unexpected data.
- Test flakiness caused by the public demo state.

## Dependency Management

Run `pip audit` periodically to check for known vulnerabilities in project dependencies. Report any high-severity findings as a private issue.
