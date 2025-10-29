import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import requests
import re

load_dotenv()
valid_url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def find_events_page(base_url:str) -> str|None:
    url_to_check = base_url

    for i in range(10): # Limit the amout of pages explored
        response = requests.get(url_to_check, allow_redirects=True)
        if response.status_code != 200: continue
        html = response.text
        
        generated_response = generate_find_events_page_response(html, url_to_check)
        if "NEWS FOUND" in generated_response.upper():
            return url_to_check
        else:
            url_to_check = generated_response

    return None

def generate_find_events_page_response(html:str, url:str) -> str:
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )
    with open("./sys_instructions/find_events.txt", "r") as f:
        sys_instructions = f.read()
    model = "gemini-2.5-flash-lite"
    generate_content_config = types.GenerateContentConfig(
        temperature=0.5,
        thinking_config = types.ThinkingConfig(
            thinking_budget=8192,
        ),
        system_instruction=[
            types.Part.from_text(text=sys_instructions),
        ],
    )

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"URL: {url}\nHTML: `{html}`"),
            ],
        ),
    ]

    content = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    return content.text
