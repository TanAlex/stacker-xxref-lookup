from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import re, logging
from stacker.session_cache import get_session
from .utils import *
import json
logger = logging.getLogger(__name__)

def handle(value, provider=None, context=None, **kwargs):
    """assume roles to different account and get stack output value.

    Arguments:
        value {str} -- full string of the lookup
            Syntax:  <tag>@<region>/<stack_name>::<output_name>
                or   <tag>/<stack_name>::<output_name>
            Example: shared@us-west-2/lisi-aero-shared-vpc::VpcId
                 or: shared/lisi-aero-shared-vpc::VpcId
        provider {:class:`stacker.provider.base.BaseProvider`} --
            subclass of the base provider
        context {:class:`stacker.context.Context`} -- stacker context

    Returns:
        output -- value of the output

    """
    if provider is None:
        raise ValueError('Provider is required')
    if context is None:
        raise ValueError('Context is required')

    tags = context.tags
    if not tags:
        raise ValueError('context.tags have to be defined')

    correct_syntax_message = """
      xxref lookup error 
      Syntax:  <tag>@<region>/<stack_name>::<output_name>
          or   <tag>/<stack_name>::<output_name>
      Eample: shared@us-west-2/lisi-aero-shared-vpc::VpcId
          or: shared/lisi-aero-shared-vpc::VpcId
    """
    regex = re.compile(
        r'(?P<tag>[\w\-]+)(@(?P<region>[\w\-]+))?/(?P<stack_name>[\w\-]+)::(?P<stack_value>[\w\-]+)'
    )
    parts = regex.search(value)
    if not parts:
        logger.error(correct_syntax_message)
        raise ValueError("xxref lookup error")        
    parts = parts.groupdict()
    logger.debug(json.dumps(parts))
    
    tag, region, stack_name, stack_value = parts['tag'], parts['region'], parts['stack_name'], parts['stack_value']
    if not region:
        region = provider.region
    if tag == "":
        logger.error("have to provide tag in the xxref lookup")
        logger.error(correct_syntax_message)
        raise ValueError("xxref lookup error")
    if not tag in tags:
        logger.error("{} is not part of available tags: {}".format(tag, tags))
        logger.error(correct_syntax_message)
        raise ValueError("xxref lookup error")

    arn = tags[tag]
    logger.debug(f"{tag}, {region}, {stack_name}, {stack_value}")

    # assume role and start a session with random session name
    session = assume_role(arn, "{}{}".format(tag, randome_string()) )
    provider = get_provider_from_session(session, region)
    output = provider.get_outputs(stack_name).get(stack_value, None)
    logger.info("xxref output: {}".format(output))
    return output