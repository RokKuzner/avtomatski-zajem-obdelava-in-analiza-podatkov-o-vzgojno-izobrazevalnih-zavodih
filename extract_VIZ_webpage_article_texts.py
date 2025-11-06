import db_manipulation as db
import requests

def extract_texts():
    for viz in db.get_all_vzgojno_izobrazevalni_zavodi():
        article_urls = db.get_articles_url_by_viz_id(viz["id"])

        for url in article_urls:
            try:
                response = requests.get(url)
            except Exception as e:
                continue

            for attempt in range(3):
                try:
                    data = generate_extract_article_text_response(response.text)
                except Exception as e:
                    continue
                if not ( "heading" in data and "content" in data ):
                    continue

                db.add_viz_webpage_article(viz["id"], data["heading"], data["content"], url)
                break

def generate_extract_article_text_response(html:str) -> list[str]:
    return []