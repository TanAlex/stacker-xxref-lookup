import boto3
from boto3.session import Session
from stacker.providers.aws.default import Provider
from stacker.session_cache import get_session

import logging 
import string, random
logger = logging.getLogger(__name__)

def assume_role(arn, session_name):
    client = boto3.client('sts')
    account_id = client.get_caller_identity()["Account"]
    logger.debug("In {}, Current account: {}".format(__name__, account_id))
    
    response = client.assume_role(RoleArn=arn, RoleSessionName=session_name)
     
    session = Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                      aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                      aws_session_token=response['Credentials']['SessionToken'])
    
    # client = session.client('sts')
    # account_id = client.get_caller_identity()["Account"]
    # logger.info("assumed account: {}".format(account_id))
    return session

def get_provider_from_session(session, region):
    return Provider(session, region)

def randome_string(length=5):
    chars = string.ascii_letters + string.digits
    parameter_value = ''.join(random.choice(chars) for _ in range(length))
    return parameter_value

from stacker.variables import Variable, resolve_variables
def get_variables(variables, provider, context):
    """Resolves lookups passed into a hook as args."""
    converted_variables = [
        Variable(k, v) for k, v in variables.items()
    ]
    resolve_variables(
        converted_variables, context, provider
    )
    return {v.name: v.value for v in converted_variables}