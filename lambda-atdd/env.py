def before_all(context):
    # Read the environment and user data
    context.env = context.config.userdata.get('env', 'default')
    if context.env == 'prod':
        context.lambda_name = 'prod-lambda-function'
    elif context.env == 'staging':
        context.lambda_name = 'staging-lambda-function'
    else:
        context.lambda_name = 'dev-lambda-function'