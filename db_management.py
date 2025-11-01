import sqlite3

connection = sqlite3.connect("database.db")

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

# Commit changes and close the connection
connection.commit()
connection.close()