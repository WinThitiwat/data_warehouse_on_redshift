import config

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events
    (
        artist VARCHAR,
        auth VARCHAR,
        firstName VARCHAR(64),
        gender CHAR,
        itemInSession INTEGER,
        lastName VARCHAR(64), 
        length DECIMAL,
        level VARCHAR,
        location VARCHAR,
        method VARCHAR,
        page VARCHAR,
        registration DECIMAL,
        sessionId INTEGER ,
        song VARCHAR,
        status INTEGER,
        ts BIGINT,
        userAgent VARCHAR,
        userId INTEGER 
    );
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs
    (
        num_songs INTEGER,
        artist_id VARCHAR,
        artist_latitude DECIMAL,
        artist_longitude DECIMAL,
        artist_location VARCHAR(512),
        artist_name VARCHAR(512),
        song_id VARCHAR,
        title VARCHAR(512),
        duration DECIMAL,
        year INTEGER
    );
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays
    (
        songplay_id INTEGER IDENTITY(1,1),
        start_time TIMESTAMP,
        user_id INTEGER,
        level VARCHAR,
        song_id VARCHAR,
        artist_id VARCHAR,
        session_id INTEGER,
        location VARCHAR,
        user_agent VARCHAR
    )
    DISTSTYLE KEY
    DISTKEY( start_time )
    SORTKEY( start_time )
    ;
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
    (
        user_id INTEGER PRIMARY KEY,
        first_name VARCHAR(64),
        last_name VARCHAR(64),
        gender CHAR,
        level VARCHAR
    )
    SORTKEY( user_id )
    ;
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs
    (
        song_id VARCHAR PRIMARY KEY,
        title VARCHAR(512),
        artist_id VARCHAR,
        year INTEGER,
        duration DECIMAL
    )
    SORTKEY( song_id );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists
    (
        artist_id VARCHAR,
        name VARCHAR(512),
        location VARCHAR(512),
        latitude DECIMAL,
        longitude DECIMAL
    )
    SORTKEY( artist_id )
    ;
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time
    (
        start_time TIMESTAMP,
        hour SMALLINT,
        day SMALLINT,
        week SMALLINT,
        month SMALLINT,
        year SMALLINT,
        weekday VARCHAR
    )
    DISTSTYLE KEY
    DISTKEY( start_time )
    SORTKEY( start_time )
    ;
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events FROM {source}
    CREDENTIALS 'aws_iam_role={iam_role}'
    STATUPDATE TRUE
    FORMAT AS JSON {source_path}
""").format(
    source=config.LOG_DATA,
    iam_role=config.IAM_ARN,
    source_path=config.LOG_JSONPATH
)

staging_songs_copy = ("""
    COPY staging_songs FROM {source}
    CREDENTIALS 'aws_iam_role={iam_role}'
    STATUPDATE TRUE
    FORMAT AS JSON 'auto'
""").format(
    source=config.SONG_DATA,
    iam_role=config.IAM_ARN
)

# FINAL TABLES
# timestamp format ref: https://www.fernandomc.com/posts/redshift-epochs-and-timestamps/
songplay_table_insert = ("""
    INSERT INTO songplays
    (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent )
    SELECT
        DISTINCT TIMESTAMP 'epoch' + (se.ts / 1000) * INTERVAL '1 second' as start_time,
        se.userId,
        se.level,
        ss.song_id,
        ss.artist_id,
        se.sessionId,
        se.location,
        se.userAgent
    FROM staging_events AS se
    INNER JOIN staging_songs AS ss
    ON se.song = ss.title AND se.artist = ss.artist_name;
""")

user_table_insert = ("""
    INSERT INTO users
    (user_id, first_name, last_name, gender, level)
    SELECT
        DISTINCT se.userId as user_id,
        se.firstName as first_name,
        se.lastName as last_name,
        se.gender,
        se.level
    FROM staging_events AS se
    WHERE se.userId IS NOT NULL
    AND se.page = 'NextSong';
""")

song_table_insert = ("""
    INSERT INTO songs
    (song_id, title, artist_id, year, duration)
    SELECT
        DISTINCT song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs
    WHERE song_id IS NOT NULL;
""")

artist_table_insert = ("""
    INSERT INTO artists
    (artist_id, name, location, latitude, longitude)
    SELECT
        DISTINCT artist_id,
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude
    FROM staging_songs;
""")

time_table_insert = ("""
    INSERT INTO time
    (start_time, hour, day, week, month, year, weekday)
    SELECT
        DISTINCT TIMESTAMP 'epoch' + (se.ts / 1000) * INTERVAL '1 second' as start_time,
        EXTRACT( hour FROM start_time) as hour,
        EXTRACT( day FROM start_time) as day,
        EXTRACT( week FROM start_time) as week,
        EXTRACT( month FROM start_time) as month,
        EXTRACT( year FROM start_time) as year,
        to_char(start_time, 'DAY')
    FROM staging_events AS se;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
