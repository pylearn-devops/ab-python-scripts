Feature: AWS Lambda and EventBridge setup

  Scenario: Check if Lambda function exists
    Given I have the Lambda function name
    When I check if the Lambda function exists
    Then the Lambda function should exist

  Scenario: Check if EventBridge rule is attached to the Lambda alias
    Given I have the Lambda function name and the rule name
    When I check if the EventBridge rule is attached to the Lambda alias "live_traffic"
    Then the EventBridge rule should be attached to the Lambda alias "live_traffic"