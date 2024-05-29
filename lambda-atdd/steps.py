import boto3
from behave import given, when, then
from botocore.exceptions import ClientError

@given('I have the Lambda function name "{lambda_name}"')
def step_given_lambda_function_name(context, lambda_name):
    context.lambda_name = lambda_name

@when('I check if the Lambda function exists')
def step_when_check_lambda_exists(context):
    client = boto3.client('lambda')
    try:
        response = client.get_function(FunctionName=context.lambda_name)
        context.lambda_exists = True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            context.lambda_exists = False
        else:
            raise e

@then('the Lambda function should exist')
def step_then_lambda_should_exist(context):
    assert context.lambda_exists, f"Lambda function {context.lambda_name} does not exist"

@given('I have the Lambda function name "{lambda_name}" and the rule name "{rule_name}"')
def step_given_lambda_function_and_rule_name(context, lambda_name, rule_name):
    context.lambda_name = lambda_name
    context.rule_name = rule_name

@when('I check if the EventBridge rule is attached to the Lambda')
def step_when_check_eventbridge_rule_attached(context):
    client = boto3.client('events')
    try:
        response = client.list_targets_by_rule(Rule=context.rule_name)
        targets = response.get('Targets', [])
        context.rule_attached = any(target['Arn'].split(':')[-1] == context.lambda_name for target in targets)
    except ClientError as e:
        context.rule_attached = False

@then('the EventBridge rule should be attached to the Lambda')
def step_then_eventbridge_rule_should_be_attached(context):
    assert context.rule_attached, f"EventBridge rule {context.rule_name} is not attached to Lambda function {context.lambda_name}"