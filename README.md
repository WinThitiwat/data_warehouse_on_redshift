# data_warehouse_on_redshift

# Overview of the project
Check out [Data Modeling with Postgres README](https://github.com/WinThitiwat/data_modeling_with_postgres/blob/master/README.md)


# Findings
## Loading S3 to Staging tables in Redshift
### `staging_events` table
- Loading time took: less than 10 seconds
- Number of records: 8056
### staging_songs
- Loading time took: approximate 2 hours
- Number of records: 385252

## Loading Staging table to Production tables in Redshift
### `songplays` table
- Loading time took: 706.981 ms
- Number of records: 6962
### `users` table
- Loading time took: 617.839 ms
- Number of records: 104
### `songs` table
- Loading time took: 833.667 ms
- Number of records: 384824
### `artists` table
- Loading time took: 695.205 ms
- Number of records: 45266
### `time` table
- Loading time took: 629.934 ms
- Number of records: 8023
# data_warehouse_on_redshift `(Still In Progress)`

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
