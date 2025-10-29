from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import db_manipulation as db

primary_school_records_url = "https://paka3.mss.edus.si/registriweb/Seznam1.aspx?Seznam=2010"
middle_school_records_url = "https://paka3.mss.edus.si/registriweb/Seznam2.aspx?Seznam=3010"

data = [
    {
        "url": primary_school_records_url,
        "name_c_n": "3",
        "web_c_n": "10",
        "label":"OS"
    },
    {
        "url": middle_school_records_url,
        "name_c_n": "1",
        "web_c_n": "8",
        "label":"SS"
    }
    ]

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
    for datapoint in data:

        driver.get(datapoint["url"])
        rows = driver.find_elements(By.CSS_SELECTOR, "#form1 > div:nth-child(19) > table > tbody > tr:nth-child(2) > td > table > tbody > tr")
        for row in rows:
            try:
                school_name = row.find_element(By.CSS_SELECTOR, f".celica:nth-child({datapoint["name_c_n"]}) > a").text
                school_website = row.find_element(By.CSS_SELECTOR, f".celica:nth-child({datapoint["web_c_n"]}) > a").get_attribute("href")

                db.add_vzgojno_izobrazevalni_zavod(datapoint["label"], school_name, school_website)
            except:
                continue

except Exception as e:
    print("Exception:", e)
finally:
    driver.quit()