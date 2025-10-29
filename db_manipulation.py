import sqlite3

def add_vzgojno_izobrazevalni_zavod(type:str, name:str, website:str) -> bool:
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        # Insert a single row
        cursor.execute("""
            INSERT INTO vzgojno_izobrazevalni_zavodi (type, name, website)
            VALUES (?, ?, ?)
        """, (type, name, website))