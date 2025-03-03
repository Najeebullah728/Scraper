import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def setup_driver():
    """Configures and returns a Selenium WebDriver with necessary options."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

def create_data_folder():
    """Creates a folder to store scraped data if it doesn't already exist."""
    if not os.path.exists("data"):
        os.makedirs("data")

def scrape_craigslist(base_url):
    """Scrapes Craigslist car listings and saves them as HTML files."""
    driver = setup_driver()
    create_data_folder()
    
    file_counter = 1
    page = 0
    
    while True:
        url = f"{base_url}&s={page}"
        print(f"Scraping: {url}")
        driver.get(url)
        
        time.sleep(10)
        
        listings = driver.find_elements(By.CLASS_NAME, "gallery-card")
        
        if not listings:
            print("No more listings found. Stopping scraper.")
            break
        
        print(f"Found {len(listings)} cars on page {(page // 120) + 1}")
        
        for listing in listings:
            html_content = listing.get_attribute("outerHTML")
            file_path = f"data/craigslist_cars_{file_counter}.html"
            
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(html_content)
            
            file_counter += 1
        
        page += 120
        time.sleep(15)
    
    driver.quit()
    print("✅ Scraping complete! Data saved in the 'data' folder.")

if __name__ == "__main__":
    url_input = "https://losangeles.craigslist.org/search/cta#search=2".strip()
    scrape_craigslist(url_input)
