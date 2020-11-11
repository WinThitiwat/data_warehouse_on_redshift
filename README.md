# data_warehouse_on_redshift `(Still In Progress)`

# Overview of the project
Check out [Data Modeling with Postgres README](https://github.com/WinThitiwat/data_modeling_with_postgres/blob/master/README.md)


### Setup Configurations File at the Root Project - dwh.config

    [AWS]
    KEY=''
    SECRET=''

    [DWH]
    DWH_CLUSTER_TYPE=''
    DWH_NUM_NODES=''
    DWH_NODE_TYPE=''
    DWH_CLUSTER_IDENTIFIER=''
    DWH_DB=''
    DWH_DB_USER=''
    DWH_DB_PASSWORD=''
    DWH_PORT=5439 # default: 5439

    [CLUSTER]
    HOST=''
    DB_NAME=''
    DB_USER=''
    DB_PASSWORD=''
    DB_PORT=''

    [IAM_ROLE]
    IAM_ROLE_NAME=''
    IAM_POLICY_ARN=''
    IAM_ROLE_DESCRIPTION=''

    [S3]
    LOG_DATA='s3://udacity-dend/log-data'
    LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
    SONG_DATA='s3://udacity-dend/song-data'
