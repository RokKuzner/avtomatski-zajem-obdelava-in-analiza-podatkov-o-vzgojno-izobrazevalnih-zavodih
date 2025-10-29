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
    
def add_events_page_url(viz_id: int, url: str):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO events_page_url (id, url)
            VALUES (?, ?)
            ON CONFLICT(id) DO UPDATE SET url = excluded.url
        """, (viz_id, url))

def get_events_page_url(viz_id:int) -> str|None:
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT url FROM events_page_url WHERE id=?", (viz_id,))
        res = cursor.fetchone()

        return res[0] if res else None