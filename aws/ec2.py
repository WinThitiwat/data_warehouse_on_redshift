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

    def is_already_existed(self, ec2_client, group_name=None):
        """
        Check if the given `group_name` already exist in the given EC2 instance

        :param ec2_client: EC2 Client object.
        :param group_name: a string of group name to be searched.

        :return True/False. Return True if the given `group_name` is found, else False.
        """
        group_info = self.get_EC2_security_group(ec2_client)[0]
        if group_info is None:
            raise Exception("Given EC2 instance not found!")
        
        if group_name is None:
            group_name = self.group_name

        return True if group_info.get(group_name) is not None else False

    def create_EC2_security_group(self, ec2_client, authorize_group=True):
        """
        Create a security group and add the specified ingress rule to the newly created security group.

        :param ec2_client: EC2 Client object
        :param authorize_group: Boolean variable telling if after creating the security group, the method should run authorize security group methods.

        :return None
        """
        try:
            if self.is_already_existed(ec2_client, self.group_name):
                aws.logger.info(f"{self.group_name} already exists!")
                return None
        except Exception as exp:
            aws.logger.info(f"Error occured while checking group existence: {exp}")
            return None

        try:
            aws.logger.info("Creating Security Group...")
            start_time = get_datetime_now()
            
            vpc_description = ec2_client.describe_vpcs()
            vpcId = vpc_description.get('Vpcs', [{}])[0].get('VpcId', '')
            
            create_secure_resp = ec2_client.create_security_group(
                GroupName=self.group_name,
                Description=self.group_description,
                VpcId=vpcId
            )
            security_group_id = create_secure_resp['GroupId']

            aws.logger.info("Creating Security Group Completed!")
            aws.logger.info("Creating Security Group Took: {millisec} ms".format(
                millisec=(get_datetime_now() - start_time).microseconds / 1000.0
            ))
            aws.logger.info(f"Creating Security Group Status: {create_secure_resp['ResponseMetadata']['HTTPStatusCode']}")
            aws.logger.info(f"Creating Security Group Info: {security_group_id} GroupID in VPC of {vpcId}")
            
            if authorize_group:
                self.authorize_security_group(ec2_client, security_group_id)

        except Exception as exp:
            aws.logger.error(f"Error occurred while creating security group: {exp}")


    def authorize_security_group(self, ec2_client, security_group_id):
        """
        Add the specified ingress rules to the given security group's ID
        
        :param ec2_client: EC2 Client object
        :param security_group_id: Security Group ID

        :return None 
        """
        try:
            if self.is_already_existed(ec2_client, self.group_name):
                aws.logger.info(f"{self.group_name} already exists!")
                return None
        except Exception as exp:
            aws.logger.info(f"Error occured while checking group existence: {exp}")
            return None

        try:
            aws.logger.info(f"Start authorizing Security Group {security_group_id}")

            start_time = get_datetime_now()
            authorize_resp = ec2_client.authorize_security_group_ingress(
                CidrIp=self.cidr_ip,
                FromPort=int(self.from_port),
                GroupId=security_group_id,
                GroupName=self.group_name,
                IpProtocol=self.ip_protocol,
                ToPort=int(self.to_port),
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

            aws.logger.info(f"Authorizing Security GroupID: {security_group_id} Completed!")
            aws.logger.info("Authorizing Security Group Took: {millisec} ms".format(
                millisec=(get_datetime_now() - start_time).microseconds / 1000.0
            ))
            aws.logger.info(f"Authorizing Security Group Status: {authorize_resp['ResponseMetadata']['HTTPStatusCode']}")
            # aws.logger.info(f"Ingress Successfullly Set {authorize_resp}")
        except Exception as exp:
            aws.logger.error(f"Error occurred while authorizing security groupId: {security_group_id} : {exp}")


    def delete_EC2_security_group(self, ec2_client):
        """
        Delete a security group based on the GroupId where it belongs to.

        :param ec2_client: EC2 Client object

        :return None
        """
        secure_group_info = self.get_EC2_security_group(ec2_client)[0]

        if secure_group_info is None:
            aws.logger.info(f"{self.group_name} group not found!")
            return None

        try:
        
            aws.logger.info(f"Deleting Security Group, Group ID: {secure_group_info['GroupId']}")

            start_time = get_datetime_now()

            delete_resp = ec2_client.delete_security_group(
                GroupId=secure_group_info['GroupId'],
                GroupName=self.group_name)

            aws.logger.info(f"Deleting Security GroupID: {secure_group_info['GroupId']} Completed!")
            aws.logger.info("Deleting Security Group Took: {millisec} ms".format(
                millisec=(get_datetime_now() - start_time).microseconds / 1000.0
            ))
            aws.logger.info(f"Deleting Security Group Status: {delete_resp['ResponseMetadata']['HTTPStatusCode']}")

        except Exception as exp:
            aws.logger.error(f"Error occurred while deleting security group: {exp}")
    