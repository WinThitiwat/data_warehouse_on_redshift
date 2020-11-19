import aws 
from . import aws_common
from .iam import IAM
from .aws_common import get_datetime_now

class Redshift(aws_common.AWS):

    def __str__(self):
        return 'redshift.Redshift object'

    def __repr__(self):
        return 'redshift.Redshift()'


    def create_Redshift_cluster(self, redshift_client, iam_client, vpc_security_group_id):
        """
        Create a new Redshift cluster where IAM information 
        is based on the dwh.cfg.

        :param redshift_client: Redshift Client object
        :param iam_client: IAM Client object
        :param vpc_security_group_id: Security Group ID

        :return None
        """
        try:
            aws.logger.info("Creating Cluster...")

            iam_role = IAM.get_IAM_ARN_role(iam_client, self.iam_role_name)
            # print(iam_role)
            start_time = get_datetime_now()

            create_cluster_resp = redshift_client.create_cluster(
                # hardware params
                ClusterType=self.dwh_cluster_type,
                NodeType=self.dwh_node_type,
                NumberOfNodes=int(self.dwh_num_nodes),

                # identifiers & credential params
                DBName=self.dwh_db,
                ClusterIdentifier=self.dwh_cluster_identifier,
                MasterUsername=self.dwh_db_user,
                MasterUserPassword=self.dwh_db_password,

                # VpcSecurityGroupIds
                VpcSecurityGroupIds=[vpc_security_group_id],

                # IAM role params
                IamRoles=[iam_role]
            )

            aws.logger.info("Creating Cluster Completed!")
            aws.logger.info("Creating Cluster Took: {millisec} ms".format(
                millisec=(get_datetime_now() - start_time).microseconds / 1000.0
            ))
            aws.logger.info(f"Creating Cluster Status: {create_cluster_resp['ResponseMetadata']['HTTPStatusCode']}")

        except Exception as exp:
            aws.logger.error(f"Error occurred while creating Redshift cluster: {exp}")

    @staticmethod
    def get_Redshift_cluster_status(redshift_client, cluster_identifier):
        """
        Get Redshift cluster status.

        :param redshift_client: Redshift Client object
        :param cluster_identifier: Redshift Cluster Identifier

        :return string of Redshift cluster status if found, else return None
        """
        try:
            return redshift_client.describe_clusters(ClusterIdentifier=cluster_identifier)['Clusters'][0]['ClusterStatus']
        except Exception as exp:
            aws.logger.error(f"Error occurred while retrieving Redshift Cluster: {exp}")
        return None

    def delete_Redshift_cluster(self, redshift_client, cluster_identifier=None):
        """
        Delete Redshift cluster.

        :param redshift_client: Redshift Client object
        :param cluster_identifier: (option) Redshift Cluster Identifier. If not provided, Redshift Cluster Identifier from the dwh.cfg will be used.

        :return None
        """
        if cluster_identifier is None:
            cluster_identifier = self.dwh_cluster_identifier

        if(len(redshift_client.describe_clusters(ClusterIdentifier=cluster_identifier)['Clusters'][0]) == 0):
            aws.logger.info(f"Redshift Cluster: {cluster_identifier} does not exist.")
            return None

        try:
            aws.logger.info("Deleting Cluster...")
            
            start_time = get_datetime_now()

            delete_cluster_resp = redshift_client.delete_cluster(ClusterIdentifier=cluster_identifier,  SkipFinalClusterSnapshot=True)

            aws.logger.info("Deleting Cluster Completed!")
            aws.logger.info("Deleting Cluster Took: {millisec} ms".format(
                millisec=(get_datetime_now() - start_time).microseconds / 1000.0
            ))
            aws.logger.info(f"Deleting Cluster Status: {delete_cluster_resp['ResponseMetadata']['HTTPStatusCode']}")

        except Exception as exp:
            aws.logger.error(f"Error occurred while deleting Redshift cluster: {exp}")

    