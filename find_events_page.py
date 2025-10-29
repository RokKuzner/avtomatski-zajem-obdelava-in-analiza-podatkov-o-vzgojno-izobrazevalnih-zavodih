import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def find_events_page(base_url:str) -> str|None:
    pass

def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    with open("./sys_instructions/find_events.txt", "r") as f:
        sys_instructions = f.read()

    model = "gemini-2.5-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.5,
        thinking_config = types.ThinkingConfig(
            thinking_budget=8192,
        ),
        system_instruction=[
            types.Part.from_text(text=sys_instructions),
        ],
    )

    content = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    return content
