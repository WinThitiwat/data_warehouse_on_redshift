from . import aws_common
from .iam import IAM

class Redshift(aws_common.AWS):

    def __str__(self):
        return 'redshift.Redshift object'

    def __repr__(self):
        return 'redshift.Redshift()'

    def create_Redshift_cluster(self, iam_client):
        try:
            redshift = aws_common.get_redshift_client()
            iam_role = IAM.get_IAM_ARN_role(iam_client, self.iam_role_name)

            response = redshift.create_cluster(
                # hardware params
                ClusterType=self.dwh_cluster_type,
                NodeType=self.dwh_node_type,
                NumberOfNodes=int(self.dwh_num_nodes),

                # identifiers & credential params
                DBName=self.dwh_db,
                ClusterIdentifier=self.dwh_cluster_identifier,
                MasterUsername=self.dwh_db_user,
                MasterUserPassword=self.dwh_db_password,

                # IAM role params
                IamRoles=[iam_role]
            )
        except Exception as exp:
            print(f"Failed to create new Redshift cluster: {exp}")

    @staticmethod
    def get_Redshift_cluster_status(redshift_client, cluster_identifier):
        return redshift_client.describe_clusters(ClusterIdentifier=cluster_identifier)['Clusters'][0]['ClusterStatus']

    @staticmethod
    def delete_Redshift_cluster(redshift_client, cluster_identifier):
        
        if(len(redshift_client.describe_clusters(ClusterIdentifier=cluster_identifier)['Clusters'][0]) == 0):
            print(f"Redshift Cluster: {cluster_identifier} does not exist.")
        try:
            redshift_client.delete_cluster(ClusterIdentifier=cluster_identifier,  SkipFinalClusterSnapshot=True)
        except Exception as exp:
            print(exp)

        print(f"Redshift Cluster: {cluster_identifier} has been successfully deleted")

