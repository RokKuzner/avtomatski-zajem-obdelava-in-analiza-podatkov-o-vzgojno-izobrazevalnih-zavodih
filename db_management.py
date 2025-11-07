import sqlite3

DATABASE_NAME = "database.db"

def manage():
    connection = sqlite3.connect(DATABASE_NAME)

    # Create a cursor object
    cursor = connection.cursor()

    # Settings
    cursor.execute("""
    PRAGMA foreign_keys = ON;
    """)

    # Create the tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vzgojno_izobrazevalni_zavodi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        name TEXT NOT NULL UNIQUE,
        website TEXT,
        municipality TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events_page_url (
        id INTEGER PRIMARY KEY,
        url TEXT,
        FOREIGN KEY (id) REFERENCES vzgojno_izobrazevalni_zavodi(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS article_urls (
        id INTEGER,
        url TEXT UNIQUE,
        FOREIGN KEY (id) REFERENCES vzgojno_izobrazevalni_zavodi(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS VIZ_website_article_texts (
        VIZ_id INTEGER,
        heading TEXT,
        content TEXT,
        source TEXT UNIQUE,
        FOREIGN KEY (VIZ_id) REFERENCES vzgojno_izobrazevalni_zavodi(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS media_article_candidates (
        VIZ_id INTEGER,
        content TEXT,
        source TEXT,
        FOREIGN KEY (VIZ_id) REFERENCES vzgojno_izobrazevalni_zavodi(id),
        UNIQUE (VIZ_id, source)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS media_articles (
        VIZ_id INTEGER,
        content TEXT,
        source TEXT,
        FOREIGN KEY (VIZ_id) REFERENCES vzgojno_izobrazevalni_zavodi(id),
        UNIQUE (VIZ_id, source)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sentiment_by_viz (
        id INTEGER UNIQUE,
        website_sentiment NUMERIC,
        media_sentiment NUMERIC,
        average_sentiment NUMERIC,
        FOREIGN KEY (id) REFERENCES vzgojno_izobrazevalni_zavodi(id)
    )
    """)

    # Commit changes and close the connection
    connection.commit()
    connection.close()