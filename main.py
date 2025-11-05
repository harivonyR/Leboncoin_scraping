# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 19:44:47 2025

@author: harivonyratefiarison
"""

from script.piloterr import leboncoin_search
from utils.leboncoin import query_builder
from datetime import datetime
from tqdm import tqdm
import json
import time

# 1. Category to scrape (see the list in output/leboncoin_categories_with_id)
categories = ["2", "3", "6"]

# 2. Search Filter
"""
    category   :  1, 2, 3, ...
    sort       :  time/price 
    order      :  asc/desc
    ad_type    :  offer/demand
    owner_type :  private/professionnel 
    urgent     :  1 (or delete if not urgent)
    price      :  10-1000 (min-max)
"""
search_param = {
    "page": "_page_",
    "category": "_category_",
    "order": "desc",
    "sort": "time",
    "ad_type": "offer"
}

# 3. Scrape & Export Data
for cat in categories:
    data = []
    page = 1
    max_page = None
    pbar = None

    while True:
        # Build URL and Fill Placeholder
        search_url = query_builder(**search_param).replace("_page_", str(page)).replace("_category_", cat)
        #print(search_url)
        # Request API
        response = leboncoin_search(search_url)
        result = json.loads(response.text)

        # Discover total pages on first request
        if max_page is None:
            max_page = result.get("max_pages", 1)
            pbar = tqdm(total=max_page, desc=f"Category {cat}", unit="page", leave=False)

        data.append(result)
        pbar.update(1)

        # Stop when all pages processed
        if page >= max_page:
            break

        page += 1
        time.sleep(5)

    pbar.close()

    # Export JSON
    today = datetime.now()
    output_path = f"output/category{cat}_{today.day}_{today.month}_{today.year}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Category {cat}: {len(data)} pages scraped.")
    print(f"📦 Exported to: {output_path}")
