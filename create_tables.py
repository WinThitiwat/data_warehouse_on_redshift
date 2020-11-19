import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drop all tables if exists from staging tables as well as dimensional
    and fact tables in Redshift cluster. Note that this is to reset 
    all tables.

    :param cur: Database cursor reference
    :param conn: Database connection instance
    
    :return None
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Create staging tables as well as dimensional and fact tables in 
    Redshift cluster if not exist.

    :param cur: Database cursor reference
    :param conn: Database connection instance
    
    :return None
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()