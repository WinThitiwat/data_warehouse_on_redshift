import aws

def main():
    awsclient = aws.AWS_Client()


    # 1. Create new IAM Role
    # iam_client = aws.get_IAM_client()
    # awsclient.create_IAM_role(iam_client)

    # 2. Create a security group to control traffic
    ec2_client = aws.get_ec2_resource()
    # print(ec2_client.describe_vpcs())
    # vpc_description = ec2_client.describe_vpcs()
    
    print(awsclient.get_EC2_security_group(ec2_client))






if __name__ == "__main__":
    main()