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
    SORTKEY( user_id );
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

""").format()

staging_songs_copy = ("""

""").format()

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
