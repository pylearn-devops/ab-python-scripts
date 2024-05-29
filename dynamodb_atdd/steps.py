import boto3
from botocore.exceptions import ClientError
from behave import given, when, then

@given('I have a DynamoDB client')
def step_impl(context):
    context.dynamodb = boto3.client('dynamodb', region_name='us-west-2')

@when('I check for the DynamoDB table named "{table_name}"')
def step_impl(context, table_name):
    context.table_name = table_name

@then('the table "{table_name}" should exist and be active in DynamoDB')
def step_impl(context, table_name):
    try:
        response = context.dynamodb.describe_table(TableName=table_name)
        assert response['Table']['TableStatus'] == 'ACTIVE', f"Table {table_name} is not active."
    except ClientError as e:
        assert False, f"Table {table_name} does not exist. Error: {e.response['Error']['Message']}"