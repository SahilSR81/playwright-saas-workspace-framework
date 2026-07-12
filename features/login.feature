Feature: Login

  Scenario: Valid login
    Given the user is on the login page
    When the user logs in with valid credentials
    Then the dashboard should be displayed
