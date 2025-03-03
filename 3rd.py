import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def setup_driver():
    """Set up Selenium WebDriver with anti-detection options."""
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)


    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def create_data_folder():
    """Create 'main_data' folder if it does not exist."""
    if not os.path.exists("main_data"):
        os.makedirs("main_data")

def scrape_links_from_csv(csv_file):
    """Reads links from CSV, clicks 'Reply' button, waits, clicks 'Call' button, waits, and scrapes data."""
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found!")
        return
    
    create_data_folder()
    driver = setup_driver()

    df = pd.read_csv(csv_file)
    links = df["link"].tolist()

    for idx, link in enumerate(links, start=1):
        try:
            print(f"Scraping: {link}")
            driver.get(link)
            time.sleep(10)  
            
    
            try:
                wait = WebDriverWait(driver, 10)
                reply_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.reply-button")))
                
       
                driver.execute_script("arguments[0].scrollIntoView(true);", reply_button)
                time.sleep(2)
                reply_button.click()
                print("✅ Clicked 'Reply' button!")

                time.sleep(10)  


                try:
                    call_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'call')]")))
                    driver.execute_script("arguments[0].scrollIntoView(true);", call_button)
                    time.sleep(6)
                    call_button.click()
                    print("✅ Clicked 'Call' button!")

                    time.sleep(12)  

                except Exception as e: 
                    print(f"⚠️ 'Call' button not found or not clickable: {e}")
            
            except Exception as e:
                print(f"⚠️ 'Reply' button not found or clickable: {e}")
            
           
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
        
            file_path = f"main_data/listing_{idx}.html"
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(str(soup))
            
            print(f"✅ Saved: {file_path}")
        
        except Exception as e:
            print(f"❌ Error with {link}: {e}")
    
    driver.quit()
    print("✅ Scraping complete! All pages saved in 'main_data' folder.")


csv_file = "craigslist_links.csv"
scrape_links_from_csv(csv_file)
