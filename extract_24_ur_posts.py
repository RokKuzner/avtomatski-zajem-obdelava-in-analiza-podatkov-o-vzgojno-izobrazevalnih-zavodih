from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import urllib.parse
import db_manipulation as db

def extract(start_indx=None, end_indx=None):
    # Setup driver for background use
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Create driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Extract articles
        for viz in db.get_all_vzgojno_izobrazevalni_zavodi()[start_indx:end_indx]:
            search_url = "https://www.24ur.com/iskanje?q=" + urllib.parse.quote_plus(viz["name"])
            print(search_url)
            try:
                driver.get(search_url)
            except Exception as e:
                with open("logs.txt", "a") as f:
                    f.write(viz["name"]+"\n"+search_url+"\n"+str(e)+"\n\n\n\n")

            article_elements = driver.find_elements(By.CSS_SELECTOR, "main.main div a.group")
            article_links = [article_element.get_attribute("href") for article_element in article_elements]
            
            # Extract actual article content
            for article_link in article_links:
                if not article_link: continue

                driver.get(article_link)

                content_elements = driver.find_elements(By.CSS_SELECTOR, "article p")[:-1] # Skip the last element, sice it is allways a non-content-realted warning
                if not content_elements: continue

                content = " ".join( [content_element.text.strip() for content_element in content_elements] )
                db.add_media_article_candidate(viz["id"], content, article_link)
    finally:
        driver.quit()