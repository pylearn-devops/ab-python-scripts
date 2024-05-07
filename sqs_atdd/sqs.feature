Feature: SQS Queue Verification

  Scenario: Verify SQS Queue Existence
    Given an SQS queue with name "my-queue" exists
    Then the SQS queue "my-queue" should exist