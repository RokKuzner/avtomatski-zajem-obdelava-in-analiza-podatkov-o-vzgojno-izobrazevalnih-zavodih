import sqlite3

connection = sqlite3.connect("database.db")

# Create a cursor object
cursor = connection.cursor()

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS vzgojno_izobrazevalni_zavodi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    website TEXT,
)
""")

# Commit changes and close the connection
connection.commit()
connection.close()