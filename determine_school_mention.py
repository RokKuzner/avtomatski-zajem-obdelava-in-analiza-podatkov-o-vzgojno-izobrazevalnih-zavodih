import db_manipulation as db
import requests
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time

load_dotenv()

def extract_texts(start_indx=None, end_indx=None):
    for article in db.get_all_media_article_candidates()[start_indx:end_indx]:
        viz = db.get_vzgojno_izobrazevalni_zavod_by_id(article["VIZ_id"])

        if not viz:
            with open("logs.txt", "a") as f:
                f.write(viz["id"]+"-"+viz["name"]+"\n"+article["source"]+"\n"+str(e)+"\n\n\n\n")
            continue

        #TODO: check if already saved

        for attempt in range(3):
            try:
                data = is_school_mentioned(viz, article["content"])
                #TODO: add to database if the school is mentioned
                print("        ✅")
            except Exception as e:
                print("        server error")
                print("            waiting")
                time.sleep(10)
                print("            🔁 retrying")
                continue

def is_school_mentioned(viz:dict, article_content:str) -> bool:
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash-lite"
    with open("./sys_instructions/determine_school_mention.txt", "r") as f:
        sys_instructions = f.read()

    generate_content_config = types.GenerateContentConfig(
        temperature=0.05,
        thinking_config = types.ThinkingConfig(
            thinking_budget=8192,
        ),
        system_instruction=[
            types.Part.from_text(text=sys_instructions)
        ],
    )

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"School name: {viz["name"]}\nSchool website url: {viz["website"]}\nSchool municipality: {viz["municipality"]}\nArticle contents:\n`{article_content}`"),
            ],
        ),
    ]

    content = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    return True if "YES" in content.text.upper() else False