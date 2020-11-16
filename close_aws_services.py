import aws

def main():
    awsclient = aws.AWS_Client()

    # ==== get all related clients service ====
    iam_client = aws.get_IAM_client()
    ec2_client = aws.get_ec2_resource(region_name='us-west-2')
    redshift_client = aws.get_redshift_client()

    # ===== delete =====
    awsclient.delete_IAM_role(iam_client)
    awsclient.delete_Redshift_cluster(redshift_client, awsclient.dwh_cluster_identifier)
    awsclient.delete_EC2_security_group(ec2_client)


if __name__ == "__main__":
    main()