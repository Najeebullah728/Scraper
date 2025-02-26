import requests
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://gist.github.com/figassis/07221d9c51f413e30b78457f69666547"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()

    phone_pattern = re.compile(r'\+?[0-9][0-9\-\.\(\)\s]{8,15}[0-9]')
    phone_numbers = phone_pattern.findall(text)

    folder_name = "data"
    os.makedirs(folder_name, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(folder_name, f"numbers_{timestamp}.txt")

    with open(file_path, "w", encoding="utf-8") as file:
        for num in set(phone_numbers):
            file.write(num + "\n")

    print(f"Extracted Phone Numbers saved in: {file_path}")
else:
    print("Failed to fetch the website!")
