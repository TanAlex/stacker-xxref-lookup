import os
import yaml
import json
import logging 

# from .utils import *
from . import utils

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

def print_result(context, provider, **kwargs):
    result = json.dumps(context.config.__dict__,
                sort_keys=True,
                indent=4,
                default=str)
    logger.debug(result)
    variables = utils.get_variables(kwargs, provider, context)
    result = json.dumps(variables,
                sort_keys=True,
                indent=4,
                default=str)
    logger.debug(result)

    return False

