def before_all(context):
    # Read the environment and user data
    context.env = context.config.userdata.get('env', 'default')
    if context.env == 'prod':
        context.lambda_name = 'prod-lambda-function'
        context.rule_name = 'prod-eventbridge-rule'
    elif context.env == 'staging':
        context.lambda_name = 'staging-lambda-function'
        context.rule_name = 'staging-eventbridge-rule'
    else:
        context.lambda_name = 'dev-lambda-function'
        context.rule_name = 'dev-eventbridge-rule'