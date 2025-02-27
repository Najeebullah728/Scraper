import os
import pandas as pd
from bs4 import BeautifulSoup

data = {"title": [], "price": [], "link": []}
folder_path = "data"

if not os.path.exists(folder_path):
    print("Error: 'data' folder not found!")
    exit()

for file_name in os.listdir(folder_path):
    if file_name.endswith(".html"):
        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                html_doc = f.read()
            
            soup = BeautifulSoup(html_doc, "html.parser")
            
            title = soup.find("span", class_="label")
            title = title.get_text(strip=True) if title else "N/A"
            
            link = soup.find("a", class_="cl-app-anchor text-only posting-title")
            link = link["href"] if link and link.has_attr("href") else "N/A"
            
            price = soup.find("span", class_="priceinfo")
            price = price.get_text(strip=True) if price else "N/A"
            
            data["title"].append(title)
            data["price"].append(price)
            data["link"].append(link)
        
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

df = pd.DataFrame(data)
df.to_csv("craigslist_cars.csv", index=False)
print("Data extraction complete! Saved in 'craigslist_cars.csv'")
