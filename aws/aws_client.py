from . import redshift
from . import s3
from . import iam

class AWS_Client(redshift.Redshift, s3.S3, iam.IAM):
    def __str__(self):
        return 'aws_client.AWS_Client object'

    def __repr__(self):
        return 'aws_client.AWS_Client()'
