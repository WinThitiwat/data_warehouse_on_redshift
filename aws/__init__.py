"""
    All methods in the `aws` package here are referenced from 
    the boto3.amazonaws.com
"""
from .iam import *
from .redshift import *
from .s3 import *
from .aws_client import *
from .aws_common import *
from .ec2 import *

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logging.getLogger(__name__).setLevel(logging.INFO)
logger = logging.getLogger(__name__)