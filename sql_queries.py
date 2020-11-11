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
        auth VARCHAR(20) NOT NULL,
        firstName VARCHAR,
        gender CHAR,
        itemInSession INTEGER NOT NULL,
        lastName VARCHAR, 
        length DECIMAL,
        level VARCHAR(10),
        location VARCHAR,
        method VARCHAR(10),
        page VARCHAR(15) NOT NULL,
        registration DECIMAL(15,2)
        sessionId INTEGER NOT NULL,
        song VARCHAR,
        status INTEGER NOT NULL,
        ts BIGINT NOT NULL,
        userAgent VARCHAR,
        userId INTEGER NOT NULL
    );
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs
    (
        num_songs INTEGER,
        artist_id VARCHAR NOT NULL,
        artist_latitude DECIMAL,
        artist_longitude DECIMAL,
        artist_location VARCHAR,
        artist_name VARCHAR,
        song_id VARCHAR NOT NULL,
        title VARCHAR,
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
        level VARCHAR NOT NULL,
        song_id VARCHAR,
        artist_id VARCHAR,
        session_id INTEGER,
        location VARCHAR,
        user_agent VARCHAR
    )
    DISTSTYLE KEY,
    DISTKEY( start_time )
    SORTKEY( start_time )
    ;
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
    (
        user_id INTEGER PRIMARY KEY,
        first_name VARCHAR,
        last_name VARCHAR,
        gender CHAR,
        level VARCHAR(10)
    )
    SORTKEY( user_id )
    ;
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs
    (
        song_id VARCHAR PRIMARY KEY,
        title VARCHAR,
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
        name VARCHAR,
        location VARCHAR,
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
    DISTSTYLE KEY,
    DISTKEY( start_time )
    SORTKEY( start_time )
    ;
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events FROM {source}
    CREDENTIALS 'aws_iam_role={iam_role}'
    JSON 'auto'
""").format(
    source=config.LOG_DATA,
    iam_role=config.IAM_ROLE_NAME
)

staging_songs_copy = ("""
    COPY staging_songs FROM {source}
    CREDENTIALS 'aws_iam_role={iam_role}'
    JSON 'auto'
""").format(
    source=config.SONG_DATA,
    iam_role=config.IAM_ROLE_NAME
)

# FINAL TABLES
# timestamp format ref: https://www.fernandomc.com/posts/redshift-epochs-and-timestamps/
songplay_table_insert = ("""
    INSERT INTO songplays
    (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent )
    SELECT
        TIMESTAMP 'epoch' + (se.ts / 1000) * INTERVAL '1 second' as start_time,
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
        userId,
        firstName,
        lastName,
        gender,
        level
    FROM staging_events
    WHERE userId NOT NULL;
""")

song_table_insert = ("""
    INSERT INTO songs
    (song_id, title, artist_id, year, duration)
    SELECT
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs
    WHERE song_id NOT NULL;
""")

artist_table_insert = ("""
    INSERT INTO artists
    (artist_id, name, location, latitude, longitude)
    SELECT
        artist_id,
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
        TIMESTAMP 'epoch' + (se.ts / 1000) * INTERVAL '1 second' as start_time,
        EXTRACT( hour FROM start_time) as hour,
        EXTRACT( day FROM start_time) as day,
        EXTRACT( week FROM start_time) as week,
        EXTRACT( month FROM start_time) as month,
        EXTRACT( year FROM start_time) as year,
        to_char(start_time, 'DAY')
    FROM staging_events;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
