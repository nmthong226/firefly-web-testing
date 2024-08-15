Feature: Firefly III Transaction Management

  Scenario: User logs into Firefly III
    Given the login page loads
    When the user fills in login details and enters
    Then the user is redirected to the dashboard

  Scenario: Create a new transaction
    Given the user is on the dashboard
    When the user navigates to create a new transaction
    Then the transaction form is displayed