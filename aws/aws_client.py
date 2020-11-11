from . import redshift
from . import s3
from . import iam
from . import ec2

class AWS_Client(redshift.Redshift, s3.S3, iam.IAM, ec2.EC2):
    def __str__(self):
        return 'aws_client.AWS_Client object'

    def __repr__(self):
        return 'aws_client.AWS_Client()'
