import json
import aws 

from . import aws_common
from .aws_common import get_datetime_now

class IAM(aws_common.AWS):
    def __str__(self):
        return 'iam.IAM object'

    def __repr__(self):
        return 'iam.IAM()'

    def create_IAM_role(self, iam_client):
        """
        Create a new IAM role and attach a role policy based on information from the dwh.cfg 

        :param iam_client: IAM Client object

        :return None
        """

        try:
            aws.logger.info("Creating IAM Role...")
            start_time = get_datetime_now()
            # create a new IAM role
            create_resp = iam_client.create_role(
                Path='/',
                RoleName=self.iam_role_name,
                Description=self.iam_role_description,
                AssumeRolePolicyDocument=json.dumps(
                    {
                        'Statement': [
                            {
                                'Action': 'sts:AssumeRole',
                                'Effect': 'Allow',
                                'Principal': {
                                    'Service': 'redshift.amazonaws.com'
                                }
                            }
                        ],
                        'Version': '2012-10-17'
                    })
            )

            aws.logger.info("Creating IAM Role Completed!")
            aws.logger.info("Creating IAM Role Took: {millisec} ms".format(
                millisec=(get_datetime_now() - start_time).microseconds / 1000.0
            ))
            aws.logger.info(f"Creating IAM Role Status: {create_resp['ResponseMetadata']['HTTPStatusCode']}")

        except Exception as exp:
            aws.logger.error(f"Error occurred while creating IAM Role: {exp}")
            return None

        try:
            aws.logger.info("Attaching Role Policy...")

            start_time = get_datetime_now()
            
            # attach policy
            attach_role_resp = iam_client.attach_role_policy(RoleName=self.iam_role_name,
                                            PolicyArn=self.iam_policy_arn,
                                            )

            aws.logger.info("Attaching Role Policy Completed!")
            aws.logger.info("Attaching Role Policy Took: {millisec} ms".format(
                millisec=(get_datetime_now() - start_time).microseconds / 1000.0
            ))
            aws.logger.info(f"Attaching Role Policy Status: {attach_role_resp['ResponseMetadata']['HTTPStatusCode']}")

        except Exception as exp:
            aws.logger.error(f"Error occurred while attaching IAM Role Policy: {exp}")
            return None
    
    @staticmethod
    def get_IAM_ARN_role(iam_client, im_role_name):
        """
        Get IAM ARN role

        :param iam_role_name: (optional) IAM Role to be deleted

        :return a string of IAM ARN Role name if given `im_role_name` found else return None 
        """
        try:
            return iam_client.get_role(RoleName=im_role_name)['Role']['Arn']
        except Exception as exp:
            aws.logger.error(f"Error occurred while retrieving IAM Role: {exp}")
        return None

    def delete_IAM_role(self, iam_client, iam_role_name=None, policy_arn=None):
        """
        Delete IAM role and detach a role policy based on information from the dwh.cfg 

        :param iam_client: IAM Client object
        :param iam_role_name: (optional) IAM Role to be deleted
        :param policy_arn: (optional) Policy ARN to be deleted

        :return None
        """
        if iam_role_name is None:
            iam_role_name = self.iam_role_name

        if policy_arn is None:
            policy_arn = self.iam_policy_arn

        try:
            aws.logger.info(f"Start deleting IAM role: {iam_role_name}...")
            aws.logger.info("Detaching Role Policy...")

            start_time = get_datetime_now()
            
            detach_resp = iam_client.detach_role_policy(RoleName=iam_role_name, PolicyArn=policy_arn)

            aws.logger.info("Detaching Role Policy Completed!")
            aws.logger.info("Detaching Role Policy Took: {millisec} ms".format(
                millisec=(get_datetime_now() - start_time).microseconds / 1000.0
            ))
            aws.logger.info(f"Detaching Role Policy Status: {detach_resp['ResponseMetadata']['HTTPStatusCode']}")

        except Exception as exp:
            aws.logger.error(f"Error occurred while detaching IAM Role: {exp}")
            return None

        try:
            aws.logger.info("Deleting Role...")

            start_time = get_datetime_now()

            delete_resp = iam_client.delete_role(RoleName=iam_role_name)

            aws.logger.info("Deleting Role Completed!")
            aws.logger.info("Deleting Role Took: {millisec} ms".format(
                millisec=(get_datetime_now() - start_time).microseconds / 1000.0
            ))
            aws.logger.info(f"Detaching Role Policy Status: {delete_resp['ResponseMetadata']['HTTPStatusCode']}")

        except Exception as exp:
            aws.logger.error(f"Error occurred while deleting IAM Role: {exp}")
            return None

        aws.logger.info(f"IAM Role: {iam_role_name} has been successfully deleted.")