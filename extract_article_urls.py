import db_manipulation as db
from dotenv import load_dotenv
import re
from urllib.parse import urljoin
from google import genai
from google.genai import types
import os
import requests

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
        # Get the events page url
        events_page_url = db.get_events_page_url(viz["id"])
        if not events_page_url: continue

        # The the page HTML
        try:
            response = requests.get(events_page_url)
        except:
            continue
        if response.status_code != 200: continue
        html = response.text

        # Get the urls to the articles
        urls = generate_extract_article_urls_response(events_page_url, html)

        for url in urls:
            db.add_article_url(viz["id"], url)

def generate_extract_article_urls_response(curent_url:str, html:str) -> list[str]:
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash-lite"
    with open("./sys_instructions/extract_article_urls.txt", "r") as f:
        sys_instructions = f.read()

    generate_content_config = types.GenerateContentConfig(
        temperature=0.5,
        thinking_config = types.ThinkingConfig(
            thinking_budget=8192,
        ),
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["urls"],
            properties = {
                "urls": genai.types.Schema(
                    type = genai.types.Type.ARRAY,
                    items = genai.types.Schema(
                        type = genai.types.Type.STRING,
                    ),
                ),
            },
        ),
        system_instruction=[
            types.Part.from_text(text=sys_instructions),
        ],
    )
    
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"URL: {curent_url}\nHTML: {html}"),
            ],
        ),
    ]

    content = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    urls:list[str] = content.parsed["urls"]
    final_urls = []

    # Validate urls
    for url in urls:
        if re.match(valid_url_regex, url):
            final_urls.append(url)
        else:
            candidate = urljoin(curent_url, url)
            if re.match(valid_url_regex, candidate):
                final_urls.append(candidate)

    return final_urls
