import json

from . import aws_common

class IAM(aws_common.AWS):
    def __str__(self):
        return 'iam.IAM object'

    def __repr__(self):
        return 'iam.IAM()'

    def create_IM_role(self, iam_client):
        try:
        # create a new IAM role
            dwhRole = iam_client.create_role(
                path='/',
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

        except Exception as exp:
            print(f"Failed to create IAM Role: {exp}")
        
        try:
            # attach policy
            iam_client.attach_role_policy(RoleName=self.iam_role_name,
                                            PolicyArn=self.iam_policy_arn,
                                            )['ResponseMetadata']['HTTPStatusCode']
        except Exception as exp:
            print(f"Failed to attach IAM Role Policy: {exp}")

    
    @staticmethod
    def get_IAM_ARN_role(iam_client, im_role_name):
        return iam_client.get_role(RoleName=im_role_name)['Role']['Arn']

    @staticmethod
    def delete_IAM_role(iam_client, iam_role_name):
        try:
            iam_client.detach_role_policy(RoleName=iam_role_name, PolicyArn='')
            iam_client.delete_role(RoleName=iam_role_name)
        except Exception as exp:
            print(exp)

        print(f"IAM Role: {iam_role_name} has been successfully deleted.")