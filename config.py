import configparser

# CONFIG init
config = configparser.ConfigParser()
config.read('dwh.cfg')

# AWS
KEY = config.get('AWS','KEY')
SECRET =config.get('AWS','SECRET')

# DWH
DWH_CLUSTER_TYPE = config.get('DWH','DWH_CLUSTER_TYPE')
DWH_NUM_NODES = config.get('DWH','DWH_NUM_NODES')
DWH_NODE_TYPE = config.get('DWH','DWH_NODE_TYPE')

DWH_CLUSTER_IDENTIFIER = config.get('DWH','DWH_CLUSTER_IDENTIFIER')
DWH_DB = config.get('DWH','DWH_DB')
DWH_DB_USER = config.get('DWH','DWH_DB_USER')
DWH_DB_PASSWORD = config.get('DWH','DWH_DB_PASSWORD')
DWH_PORT = config.get('DWH','DWH_PORT')

# SECURITY_GROUP
GROUP_NAME = config.get('SECURITY_GROUP','GROUP_NAME')
GROUP_DESCRIPTION = config.get('SECURITY_GROUP','GROUP_DESCRIPTION')

# INGRESS_RULE
CIDR_IP = config.get('INGRESS_RULE','CIDR_IP')
INGRESS_DESCRIPTION = config.get('INGRESS_RULE','INGRESS_DESCRIPTION')
IP_PROTOCOL = config.get('INGRESS_RULE','IP_PROTOCOL')
FROM_PORT = config.get('INGRESS_RULE','FROM_PORT')
TO_PORT = config.get('INGRESS_RULE','TO_PORT')

# CLUSTER
HOST = config.get('CLUSTER','HOST')
DB_NAME = config.get('CLUSTER','DB_NAME')
DB_USER = config.get('CLUSTER','DB_USER')
DB_PASSWORD = config.get('CLUSTER','DB_PASSWORD')
DB_PORT = config.get('CLUSTER','DB_PORT')

# IAM_ROLE
IAM_ROLE_NAME = config.get('IAM_ROLE','IAM_ROLE_NAME')
IAM_POLICY_ARN = config.get('IAM_ROLE','IAM_POLICY_ARN')
IAM_ROLE_DESCRIPTION = config.get('IAM_ROLE','IAM_ROLE_DESCRIPTION')
IAM_ARN = config.get('IAM_ROLE','IAM_ARN')

# S3
LOG_DATA = config.get('S3', 'LOG_DATA')
LOG_JSONPATH = config.get('S3', 'LOG_JSONPATH')
SONG_DATA = config.get('S3', 'SONG_DATA')