import configparser
import psycopg2
import datetime
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    This is to `COPY` data from S3 into staging tables in Redshift cluter.

    :param cur: Database cursor reference
    :param conn: Database connection instance
    
    :return None
    """
    total_queries = len(copy_table_queries)
    print(f"There are {total_queries} tables to load")

    for idx, query in enumerate(copy_table_queries):
        print(f"Loading table: {idx+1}/{total_queries}")
        print(f"{query}")
        
        start_time = datetime.datetime.now()
        cur.execute(query)
        conn.commit()

        print("Loading took: {millisec} ms.".format(
            millisec=(datetime.datetime.now() - start_time).microseconds / 1000.0
        ))


def insert_tables(cur, conn):
    """
    This is to run all `INSERT INTO TABLE` manipulating queries to 
    insert all data from the staging tables into the dimensional and 
    fact tables in Redshift cluster.

    :param cur: Database cursor reference
    :param conn: Database connection instance
    
    :return None
    """
    total_queries = len(insert_table_queries)
    print(f"There are {total_queries} tables to insert")

    for idx, query in enumerate(insert_table_queries):
        print(f"Inserting table: {idx+1}/{total_queries}")
        print(f"{query}")

        start_time = datetime.datetime.now()
        cur.execute(query)
        conn.commit()

        print("Loading took: {millisec} ms.".format(
            millisec=(datetime.datetime.now() - start_time).microseconds / 1000.0
        ))


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    print("connecting to Redshift")
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    print("Start loading S3 to Staging tables...")
    load_staging_tables(cur, conn)

    print("Start loading Staging tables to Production tables...")
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()