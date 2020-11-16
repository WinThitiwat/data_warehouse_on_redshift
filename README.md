# data_warehouse_on_redshift


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