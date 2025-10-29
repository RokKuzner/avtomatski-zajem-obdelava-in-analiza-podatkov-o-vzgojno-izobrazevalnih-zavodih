from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import selenium

primary_school_records_url = "https://paka3.mss.edus.si/registriweb/Seznam1.aspx?Seznam=2010"
middle_school_records_url = "https://paka3.mss.edus.si/registriweb/Seznam2.aspx?Seznam=3010"

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
    # Primary school
    driver.get(primary_school_records_url)
    schools = driver.find_elements(By.CSS_SELECTOR, "#form1 > div:nth-child(19) > table > tbody > tr:nth-child(2) > td > table > tbody > tr")[1:]
    for school in schools:
        school_name = school.find_element(By.CSS_SELECTOR, ".celica:nth-child(3) > a").text
        school_website = school.find_element(By.CSS_SELECTOR, ".celica:nth-child(10) > a").get_attribute("href")
    
except Exception as e:
    print("Exception:", e)
finally:
    driver.quit()