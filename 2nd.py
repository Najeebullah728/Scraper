import os
import pandas as pd
from bs4 import BeautifulSoup
links = []
folder_path = "data"


if not os.path.exists(folder_path):
    print("Error: The 'data' folder is missing!")
    exit()

for file_name in os.listdir(folder_path):
    if file_name.endswith(".html"):
        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            soup = BeautifulSoup(content, "html.parser")
            link_tag = soup.find("a", href=True) 
            
            if link_tag:
                links.append(link_tag["href"])
        
        except Exception as e:
            print(f"Could not process {file_name}: {e}")


df = pd.DataFrame({"link": links})
df.to_csv("craigslist_links.csv", index=False)

print("✅ Links extracted and saved in 'craigslist_links.csv'.")
 