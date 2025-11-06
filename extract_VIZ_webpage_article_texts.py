import db_manipulation as db
import requests
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time

load_dotenv()

def extract_texts(start_indx=None, end_indx=None):
    for viz in db.get_all_vzgojno_izobrazevalni_zavodi()[start_indx:end_indx]:
        print(viz["name"])
        article_urls = db.get_articles_url_by_viz_id(viz["id"])

        for url in article_urls:
            print(f"    {url}")
            try:
                response = requests.get(url)
            except Exception as e:
                with open("logs.txt", "a") as f:
                    f.write(viz["name"]+"\n"+url+"\n"+str(e)+"\n\n\n\n")
                print("        ❌ error")
                continue

            for attempt in range(3):
                try:
                    data = generate_extract_article_text_response(response.text)
                    db.add_viz_webpage_article(viz["id"], data["heading"], data["content"], url)
                except Exception as e:
                    print("        server error")
                    print("            waiting")
                    time.sleep(10)
                    print("            🔁 retrying")
                    continue

                print("        ✅")
                break

def generate_extract_article_text_response(html:str) -> list[str]:
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash-lite"
    with open("./sys_instructions/extract_article_content.txt", "r") as f:
        sys_instructions = f.read()

    generate_content_config = types.GenerateContentConfig(
        temperature=0.15,
        thinking_config = types.ThinkingConfig(
            thinking_budget=8192,
        ),
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["heading", "content"],
            properties = {
                "heading": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "content": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
            },
        ),
        system_instruction=[
            types.Part.from_text(text=sys_instructions)
        ],
    )

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"HTML: {html}"),
            ],
        ),
    ]

    content = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    return {
        "heading": content.parsed["heading"],
        "content": content.parsed["content"]
    }