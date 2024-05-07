from behave import given, then
import boto3

@given('an SQS queue with name "{queue_name}" exists')
def step_impl(context, queue_name):
    context.queue_name = queue_name
    context.aws_client = boto3.client('sqs')

@then('the SQS queue "{queue_name}" should exist')
def step_impl(context, queue_name):
    queues = context.aws_client.list_queues(QueueNamePrefix=queue_name)
    assert queue_name in queues.get('QueueUrls', []), f"{queue_name} does not exist"