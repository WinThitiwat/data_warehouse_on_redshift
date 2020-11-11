import aws 

from . import aws_common
from .iam import IAM
from .aws_common import get_datetime_now


class EC2(aws_common.AWS):
    # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-security-group.html
    def __str__(self):
        return 'ec2.EC2 object'

    def __repr__(self):
        return 'ec2.EC2()'

    def get_EC2_security_group(self, ec2_client):
        """
        Get EC2 Security Group

        :param ec2_client: EC2 Client object.

        :return: A list of EC2 security group if found, else return None.
        """
        result =  ec2_client.describe_security_groups()["SecurityGroups"]
        return result if len(result) > 0 else None

    def create_EC2_security_group(self, ec2_client):
        """
        Create a security group and add the specified ingress rule to the newly created security group.

        :param ec2_client: EC2 Client object

        :return None
        """
        try:
            aws.logger.info("Creating Security Group...")

            start_time = get_datetime_now()
            vpc_description = ec2_client.describe_vpcs()
            vpcId = vpc_description.get('Vpcs', [{}])[0].get('VpcId', '')

            create_secure_resp = ec2_client.create_security_group(
                GroupName='',
                Description='',
                VpcId=vpcId
            )
            security_group_id = create_secure_resp['GroupId']

            aws.logger.info("Creating Security Group Completed!")
            aws.logger.info("Creating Security Group Took: {millisec} ms".format(
                millisec=(get_datetime_now() - start_time).microseconds / 1000.0
            ))
            
            aws.logger.info(f"Creating Security Group Status: {create_secure_resp['ResponseMetadata']['HTTPStatusCode']}")
            aws.logger.info(f"Security Group Created Info: {security_group_id} in vpc {vpcId}")
            aws.logger.info(f"Authorizing Security Group {security_group_id}")

            start_time = get_datetime_now()

            authorize_resp = ec2_client.authorize_security_group_ingress(
                CidrIp='',
                FromPort='',
                GroupId=security_group_id,
                GroupName='',
                IpProtocol='',
                ToPort=''
                # IpPermissions=[
                #     {
                #         'FromPort':'',
                #         'IpProtocol':'',
                #         'IpRanges':[
                #             {
                #                 'CidrIp': '',
                #                 'Description': ''
                #             }
                #         ]
                #     }
                # ]
            )

            aws.logger.info(f"Authorizing Security Group {security_group_id} Completed!")
            aws.logger.info("Authorizing Security Group Took: {millisec} ms".format(
                millisec=(get_datetime_now() - start_time).microseconds / 1000.0
            ))
            aws.logger.info(f"Authorizing Security Group Status: {authorize_resp['ResponseMetadata']['HTTPStatusCode']}")
            aws.logger.info(f"Ingress Successfullly Set {authorize_resp}")



        except Exception as exp:
            aws.logger.error(f"Error occurred while creating security group: {exp}")

    def delete_EC2_security_group(self, ec2_client):
        """
        Delete a security group based on the GroupId where it belongs to.

        :param ec2_client: EC2 Client object

        :return None
        """
        secure_group_info = self.get_EC2_security_group(ec2_client)[0]
        try:
        
            aws.logger.info(f"Deleting Security Group, Group ID: {['GroupId']}")

            start_time = get_datetime_now()

            delete_resp = ec2_client.delete_security_group(GroupId=secure_group_info['GroupId'])

            aws.logger.info(f"Deleting Security Group {secure_group_info['GroupId']} Completed!")
            aws.logger.info("Deleting Security Group Took: {millisec} ms".format(
                millisec=(get_datetime_now() - start_time).microseconds / 1000.0
            ))
            aws.logger.info(f"Deleting Security Group Status: {delete_resp['ResponseMetadata']['HTTPStatusCode']}")

        except Exception as exp:
            aws.logger.error(f"Error occurred while deleting security group: {exp}")
    