import config
from . import aws_common

class S3(aws_common.AWS):
    def __str__(self):
        return 's3.S3 object'

    def __repr__(self):
        return 's3.S3()'