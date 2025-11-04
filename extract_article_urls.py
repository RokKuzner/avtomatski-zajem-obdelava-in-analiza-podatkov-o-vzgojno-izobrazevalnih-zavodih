import db_manipulation as db
from dotenv import load_dotenv
import re
from urllib.parse import urljoin
from google import genai
from google.genai import types
import os

load_dotenv()
valid_url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def extract_article_urls():
    for viz in db.get_all_vzgojno_izobrazevalni_zavodi():
        events_page_url = db.get_events_page_url(viz["id"])
        if not events_page_url: continue

        urls = generate_extract_article_urls_response("url", "html")

        for url in urls:
            db.add_article_url(viz["id"], url)

def generate_extract_article_urls_response(curent_url:str, html:str) -> list[str]:
    return []