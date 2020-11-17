# Table of Contents
1. [Overview of the project](#overview-of-the-project)
2. [Datasets](#datasets)
3. [Database Schema](#database-schema)
4. [ETL Findings](#etl-findings)
5. [Project Files](#project-files)
6. [Project Setup](#project-setup)
7. [How to Run](#how-to-run)
8. [Project Author](#project-author)

# Overview of the project
This is to simulate a situation that a music startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results. So, this project aims to:

- To build an ETL pipeline that extract data from S3, and stages them in Redshift.
- To transform staging data into a set of dimentional tables and load back in Redshift.

## **Datasets**

### **Song Data**
Song dataset is a subset of real data from the [Million Song Dataset](http://millionsongdataset.com/). The data is in JSON format and contains metadata about a song and the artist of that song.

Sample Song Data:
```
{"num_songs":1,"artist_id":"ARD7TVE1187B99BFB1","artist_latitude":null,"artist_longitude":null,"artist_location":"California - LA","artist_name":"Casual","song_id":"SOMZWCG12A8C13C480","title":"I Didn't Mean To","duration":218.93179,"year":0}
```
### **Log Data**
Log dataset is in JSON format generated by this [event simulator](https://github.com/Interana/eventsim) based on the songs in the dataset above.

Sample Log Data:
```
{"artist":"Des'ree","auth":"Logged In","firstName":"Kaylee","gender":"F","itemInSession":1,"lastName":"Summers","length":246.30812,"level":"free","location":"Phoenix-Mesa-Scottsdale, AZ","method":"PUT","page":"NextSong","registration":1540344794796.0,"sessionId":139,"song":"You Gotta Be","status":200,"ts":1541106106796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/35.0.1916.153 Safari\/537.36\"","userId":"8"}
```

## **Database Schema**
In this project, the database schema is based on the star schema, which includes Fact table and Dimension tables.
### Fact table:
- `songplays` - records in log data associated with song plays i.e. records with page `NextSong`
  
  ```
  songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
  ```
  

### Dimension tables:
- `users` - users in the app

  ```
  user_id, first_name, last_name, gender, level
  ```
  
- `songs` - songs in music database
  
  ```
  song_id, title, artist_id, year, duration
  ```
  
- `artists` - artists in music database
  
  ```
  artist_id, name, location, latitude, longitude
  ```
  
- `time` - timestamps of records in <strong>songplays</strong> broken down into specific units
  
  ```
  start_time, hour, day, week, month, year, weekday
  ```

## **ETL Findings**
### Loading S3 to Staging tables in Redshift
#### `staging_events` table
- Loading time took: less than 10 seconds
- Number of records: 8056
#### `staging_songs` table
- Loading time took: approximate 2 hours
- Number of records: 385252

### Loading Staging table to Production tables in Redshift
#### `songplays` table
- Loading time took: 706.981 ms
- Number of records: 6962
#### `users` table
- Loading time took: 617.839 ms
- Number of records: 104
#### `songs` table
- Loading time took: 833.667 ms
- Number of records: 384824
#### `artists` table
- Loading time took: 695.205 ms
- Number of records: 45266
#### `time` table
- Loading time took: 629.934 ms
- Number of records: 8023

## **Project Files**
- `aws/` - AWS Python wrapper package
- `sql_queries.py` - a Python file containing a set of data definition and data manipulation SQL commands for fact table and dimension tables
- `create_tables.py` - a Python file establishing the <strong>sparkify</strong> database connection and creating fact table and dimension tables
- `etl.py` - a Python file implementing the actual ETL data pipeline process for all datasets
- `requirements.txt` - a text file containing all mandatory dependencies for the project


## **Project Setup**
1: After cloning and navigating to the root directory for the project, make sure your system has `Python3` and `pip3` installed already. Check in Terminal by
```
$ which python3
$ which pip3
```
2: Install virtualenv using pip
```
$ pip3 install virtualenv
```
3: From the project directory, create a new virtual environment for ths project and then activate.
```
$ virtualenv venv
$ source venv/bin/activate
```
4: Install project dependencies
```
$ pip3 install -r requirements.txt
```

5: Setup Configurations File at the Root Project - `dwh.config`

    [AWS] # AWS IAM Credential
    KEY=''
    SECRET=''
    
    [DWH] # Redshift config
    DWH_CLUSTER_TYPE='' # i.e. multi-node
    DWH_NUM_NODES='' # i.e. 4
    DWH_NODE_TYPE='' # i.e. dc2.large
    DWH_CLUSTER_IDENTIFIER=''
    DWH_DB=''
    DWH_DB_USER=''
    DWH_DB_PASSWORD=''
    DWH_PORT=5439 # default: 5439
    
    [SECURITY_GROUP] # EC2 Security Group config
    GROUP_NAME=''
    GROUP_DESCRIPTION=''
    
    [INGRESS_RULE] # EC2 Inbound Rule (ingress rule) config
    CIDR_IP='' # i.e. 0.0.0.0/0
    INGRESS_DESCRIPTION=''
    IP_PROTOCOL='' # i.e. TCP
    FROM_PORT=5439 # default: 5439
    TO_PORT=5439 # default: 5439

    [CLUSTER] # Redshift Endpoint info
    HOST='' # 
    DB_NAME=''
    DB_USER=''
    DB_PASSWORD=''
    DB_PORT=''

    [IAM_ROLE] # IAM Role config
    IAM_ROLE_NAME='' #
    IAM_POLICY_ARN='' # i.e. arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
    IAM_ROLE_DESCRIPTION=''
    IAM_ARN='' # i.e. arn:aws:iam::xxxxxxxxxxxx:role/<role_name>
    
    [S3] # data source
    LOG_DATA='s3://udacity-dend/log-data'
    LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
    SONG_DATA='s3://udacity-dend/song-data'


## **How to run**
Note that if you have no AWS IAM role, EC2 Security Group, and Redshift Cluster yet, you can also create them using this project AWS Python wrapper package (`aws`)
- To create and enable IAM role, EC2 Security Group, and Redshift Cluster
```
$ python3 run_aws_services.py 
```
- To close and delete IAM role, EC2 Security Group, and Redshift Cluster
```
$ python3 close_aws_services.py 
```
#### After setting up your AWS IAM role, EC2 Security Group, and Redshift Cluster
1. Run `create_tables.py` first to create database connection and create empty fact and dimension tables
```
$ python3 create_tables.py
```
2. Run `etl.py` to perform ETL process and load all song and log data into the database tables.
```
$ python3 etl.py
```


## **Project Author**
- Author: Thitiwat Watanajaturaporn 
- Note: this project is part of Udacity's Data Engineering Nanodegree Program.

