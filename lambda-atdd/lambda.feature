Feature: AWS Lambda and EventBridge setup

  Scenario: Check if Lambda function exists
    Given I have the Lambda function name "my-lambda-function"
    When I check if the Lambda function exists
    Then the Lambda function should exist

  Scenario: Check if EventBridge rule is attached to the Lambda
    Given I have the Lambda function name "my-lambda-function" and the rule name "my-eventbridge-rule"
    When I check if the EventBridge rule is attached to the Lambda
    Then the EventBridge rule should be attached to the Lambda