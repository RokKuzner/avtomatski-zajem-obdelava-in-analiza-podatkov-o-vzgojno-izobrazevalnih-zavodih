import sqlite3
import re

def normalize_whitespace(text: str) -> str:
    normalized = re.sub(r'\s+', ' ', text)

    return normalized.strip()

def add_vzgojno_izobrazevalni_zavod(type:str, name:str, website:str, municipality:str) -> bool:
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO vzgojno_izobrazevalni_zavodi (type, name, website, municipality)
            VALUES (?, ?, ?, ?)
        """, (type, name, website, municipality))

def get_all_vzgojno_izobrazevalni_zavodi() -> list[dict]:
    with sqlite3.connect("database.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM vzgojno_izobrazevalni_zavodi")

        return [ dict(row) for row in cursor.fetchall() ]
    
def get_vzgojno_izobrazevalni_zavod_by_name(name:str) -> dict:
    with sqlite3.connect("database.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM vzgojno_izobrazevalni_zavodi WHERE name=?", (name,))
        res = cursor.fetchone()

        if res: return dict(res)
        else: return None
    
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

def add_article_url(viz_id:int, article_url:str):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO article_urls (id, url)
            VALUES (?, ?)
        """, (viz_id, article_url))

def get_articles_url_by_viz_id(viz_id:int):
    with sqlite3.connect("database.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM article_urls WHERE id=?", (viz_id,))
        res = cursor.fetchone()

        if res: return dict(res)
        else: return None

def add_viz_webpage_article(viz_id:int, heading:str, content:str, source:str):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO VIZ_website_article_texts (VIZ_id, heading, content, source)
            VALUES (?, ?, ?, ?)
        """, (viz_id, normalize_whitespace(heading), normalize_whitespace(content), source))