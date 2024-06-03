import os
import logging
import json

LOG_FORMAT = os.getenv('LOG_FORMAT', 'json')

if LOG_FORMAT == 'json':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger()

    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                'message': record.getMessage(),
                'level': record.levelname,
                'time': record.created
            }
            return json.dumps(log_record)

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
else:
    logging.basicConfig(level=logging.INFO)

def handler(event, context):
    logger.info('This is a log message')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }