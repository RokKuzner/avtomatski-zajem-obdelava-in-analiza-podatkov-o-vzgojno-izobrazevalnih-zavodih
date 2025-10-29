import sqlite3

def add_vzgojno_izobrazevalni_zavod(type:str, name:str, website:str) -> bool:
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        # Insert a single row
        cursor.execute("""
            INSERT INTO vzgojno_izobrazevalni_zavodi (type, name, website)
            VALUES (?, ?, ?)
        """, (type, name, website))

def get_all_vzgojno_izobrazevalni_zavodi() -> list[dict]:
    with sqlite3.connect("database.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Insert a single row
        cursor.execute("SELECT * FROM vzgojno_izobrazevalni_zavodi")

        return [ dict(row) for row in cursor.fetchall() ]
    
def add_events_page_url(viz_id:int, url:str):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        # Insert a single row
        cursor.execute("""
            INSERT INTO events_page_url (id, url)
            VALUES (?, ?)
        """, (viz_id, url))
