import boto3
from behave import given, when, then
from botocore.exceptions import ClientError

@given('I have the Lambda function name')
def step_given_lambda_function_name(context):
    assert context.lambda_name, "Lambda function name is not set"

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

@given('I have the Lambda function name and the rule name "{rule_name}"')
def step_given_lambda_function_and_rule_name(context, rule_name):
    assert context.lambda_name, "Lambda function name is not set"
    context.rule_name = rule_name

@when('I check if the EventBridge rule is attached to the Lambda alias "live_traffic"')
def step_when_check_eventbridge_rule_attached_to_alias(context):
    client = boto3.client('events')
    lambda_client = boto3.client('lambda')

    # Get the full ARN for the Lambda alias
    try:
        alias_response = lambda_client.get_alias(FunctionName=context.lambda_name, Name='live_traffic')
        alias_arn = alias_response['AliasArn']
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            context.alias_exists = False
            context.rule_attached = False
            return
        else:
            raise e

    context.alias_exists = True

    # Check if the EventBridge rule targets the Lambda alias ARN
    try:
        response = client.list_targets_by_rule(Rule=context.rule_name)
        targets = response.get('Targets', [])
        context.rule_attached = any(target['Arn'] == alias_arn for target in targets)
    except ClientError as e:
        context.rule_attached = False

@then('the EventBridge rule should be attached to the Lambda alias "live_traffic"')
def step_then_eventbridge_rule_should_be_attached_to_alias(context):
    assert context.alias_exists, f"Lambda alias 'live_traffic' does not exist for function {context.lambda_name}"
    assert context.rule_attached, f"EventBridge rule {context.rule_name} is not attached to Lambda alias 'live_traffic' for function {context.lambda_name}"