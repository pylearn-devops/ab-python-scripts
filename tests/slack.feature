Feature: Generate JSON from PagerDuty data

  Scenario: Generate JSON for on-call users
    Given the following escalation policies:
      | policy_id |
      | P1        |
    And the following users:
      | user_id | name     | email            |
      | U1      | User One | user1@example.com|
      | U2      | User Two | user2@example.com|
    When I generate the JSON from PagerDuty data
    Then the result should contain the policy and user details
    And the Slack message should be sent with the correct details