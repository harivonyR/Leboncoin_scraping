# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 19:44:47 2025

@author: harivonyratefiarison

"""

from script.piloterr import leboncoin_search
from utils.leboncoin import query_builder
from tqdm import tqdm
import json
import time
from datetime import datetime
import os

# Settings
category = "2"

data = []
page = 1
max_page = None  # unknown at start

# Initial request to determine total pages
init_url = query_builder(
    page=page,
    category=category,
    order="desc",
    sort="price",
    urgent="1"
)
response = leboncoin_search(init_url)
result = json.loads(response.text)
max_page = result.get("max_pages", 1)
print(f"Total pages to scrape: {max_page}")

# Add first page result
data.append(result)

# Scrape with tqdm progress bar
for page in tqdm(range(2, max_page + 1), desc="Scraping Leboncoin", unit="page"):
    search_url = query_builder(
        page=page,
        category=category,
        order="desc",
        sort="price",
        urgent="1"
    )

    try:
        response = leboncoin_search(search_url)
        result = json.loads(response.text)
        data.append(result)
        time.sleep(2)  # prevent rate limit
    except json.JSONDecodeError:
        tqdm.write(f"❌ JSON decoding error on page {page}")
        continue
    except Exception as e:
        tqdm.write(f"❌ Request failed on page {page}: {e}")
        break

# Export JSON
today = datetime.now()
output_path = f"output/category_{category}_{today.day}_{today.month}_{today.year}.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Scraping completed: {len(data)} pages retrieved")
print(f"📦 Data exported to: {output_path}")
