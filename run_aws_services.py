import aws

def main():
    awsclient = aws.AWS_Client()

    # create
    ## 1. Create new IAM Role
    iam_client = aws.get_IAM_client()
    awsclient.create_IAM_role(iam_client)
    
    ## 2. Create a security group to control traffic
    ec2_client = aws.get_ec2_resource(region_name='us-west-2')
    awsclient.create_EC2_security_group(ec2_client)
    
    ## 3. Create Redshift cluster
    security_group_id = awsclient.get_EC2_security_group(ec2_client)[0].get("GroupId")
    redshift_client = aws.get_redshift_client()
    awsclient.create_Redshift_cluster(redshift_client, iam_client, security_group_id)
    
if __name__ == "__main__":
    main()