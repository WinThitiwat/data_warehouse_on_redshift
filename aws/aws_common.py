import config
import boto3
import datetime 

class AWS(object):
    """
        AWS base class containing all common attributes that other AWS services would need to utilize.
    """
    def __init__(self) -> None:
        self.key = config.KEY
        self.secret = config.SECRET

        # DWH
        self.dwh_cluster_type = config.DWH_CLUSTER_TYPE
        self.dwh_num_nodes = config.DWH_NUM_NODES
        self.dwh_node_type = config.DWH_NODE_TYPE

        self.dwh_cluster_identifier = config.DWH_CLUSTER_IDENTIFIER
        self.dwh_db = config.DWH_DB
        self.dwh_db_user = config.DWH_DB_USER
        self.dwh_db_password = config.DWH_DB_PASSWORD
        self.dwh_port = config.DWH_PORT

        # SECURITY_GROUP
        self.group_name = config.GROUP_NAME 
        self.group_description = config.GROUP_DESCRIPTION 

        # INGRESS_RULE
        self.cidr_ip = config.CIDR_IP
        self.ingress_description = config.INGRESS_DESCRIPTION
        self.ip_protocol = config.IP_PROTOCOL
        self.from_port = config.FROM_PORT
        self.to_port = config.TO_PORT

        # CLUSTER
        self.host = config.HOST
        self.db_name = config.DB_NAME
        self.db_user = config.DB_USER
        self.db_password = config.DB_PASSWORD
        self.db_port = config.DB_PORT

        # IAM_ROLE
        self.iam_role_name = config.IAM_ROLE_NAME
        self.iam_policy_arn = config.IAM_POLICY_ARN
        self.iam_role_description = config.IAM_ROLE_DESCRIPTION
        self.iam_arn = config.IAM_ARN

        # S3
        self.log_data = config.LOG_DATA
        self.log_jsonpath = config.LOG_JSONPATH
        self.song_data = config.SONG_DATA

        # print('aws_common init completed')


def get_ec2_resource(region_name='us-west-2'):
    """
    Get EC2 Resource.

    :param region_name: default is `us-west-2`
    """
    return boto3.client('ec2',
                            region_name=region_name,
                            aws_access_key_id=config.KEY,
                            aws_secret_access_key=config.SECRET)

def get_s3_resource(region_name='us-west-2'):
    """
    Get S3 Resource.
    
    :param region_name: default is `us-west-2`
    """
    return boto3.resource('s3',
                            region_name=region_name,
                            aws_access_key_id=config.KEY,
                            aws_secret_access_key=config.SECRET)

def get_IAM_client(region_name='us-west-2'):
    """
    Get IAM Client.
    
    :param region_name: default is `us-west-2`
    """
    return boto3.client('iam',
                            region_name=region_name,
                            aws_access_key_id=config.KEY,
                            aws_secret_access_key=config.SECRET)

def get_redshift_client(region_name='us-west-2'):
    """
    Get Redshift
    
    :param region_name: default is `us-west-2`
    """
    return boto3.client('redshift',
                            region_name=region_name,
                            aws_access_key_id=config.KEY,
                            aws_secret_access_key=config.SECRET)

def get_datetime_now():
    return datetime.datetime.now()