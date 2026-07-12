Feature: Admin Search

  Scenario: Search existing user
    Given the user is logged in
    When the user searches for "Admin"
    Then search results should be displayed
