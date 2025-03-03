import os
import pandas as pd
from bs4 import BeautifulSoup

def extract_data_from_html(html_file):
    """Extract Title, Price, and Phone Number from a scraped HTML file."""
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")


    title_tag = soup.find("span", {"id": "titletextonly"}) 
    title = title_tag.text.strip() if title_tag else "N/A"

    price_tag = soup.find("span", {"class": "price"})
    price = price_tag.text.strip() if price_tag else "N/A"

  
    phone_tag = soup.select_one(".reply-content-phone a[href^='tel:']")
    phone_number = phone_tag.text.strip() if phone_tag else "N/A"

    return title, price, phone_number

def convert_scraped_data_to_csv(csv_file, output_csv="output_data.csv"):
    """Reads scraped HTML files, extracts data, and saves to CSV."""
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found!")
        return
    

    df = pd.read_csv(csv_file)
    links = df["link"].tolist()


    extracted_data = []

    for idx, link in enumerate(links, start=1):
        html_file = f"main_data/listing_{idx}.html"
        
        if os.path.exists(html_file):
            title, price, phone_number = extract_data_from_html(html_file)
            extracted_data.append([title, price, phone_number, link])
            print(f"✅ Extracted from {html_file}")
        else:
            print(f"⚠️ File not found: {html_file}")

    output_df = pd.DataFrame(extracted_data, columns=["Title", "Price", "Phone Number", "Link"])
    output_df.to_csv(output_csv, index=False, encoding="utf-8")
    
    print(f"✅ Data saved to '{output_csv}'")

csv_file = "craigslist_links.csv"
convert_scraped_data_to_csv(csv_file)
