# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 17:44:28 2025

@author: harivonyratefiarison

"""


import json
from typing import List, Dict, Any
from script.piloterr import leboncoin_search
import pandas as pd
from urllib.parse import urlencode

def query_builder(**kwargs):
    """
    Build a Leboncoin search query dynamically from non-null parameters.
    
    category   :  1, 2, 3, ...
    sort       :  time/price 
    order      :  asc/desc
    ad_type    :  offer/demand
    owner_type :  private/professionnel 
    urgent     :  1 or None
    price      :  10-1000 (min-max)
    
    sample query : https://www.leboncoin.fr/recherche?category=1&ad_type=demand&urgent=1&owner_type=pro&sort=price&order=desc
    """

    base_url = "https://www.leboncoin.fr/recherche?"

    # replace placeholder before encoding
    params = {k: v for k, v in kwargs.items() if v not in [None, ""]}
    return f"{base_url}&{urlencode(params, doseq=True)}"


def get_category_list(max_jump: int = 5, max_cat: int = 100) -> List[Dict[str, Any]]:
    """
    build a list of the result of all first page of catogier with range 1 to max_cat 
    """
    base_url = "https://www.leboncoin.fr/recherche?category={cat_id}"
    ads_all: List[Dict[str, Any]] = []
    category_list: List[Dict[str, Any]] = []
    jump = 0

    print("Scraping leboncoin categories — aggregation of all ads")
    for i in range(1, max_cat + 1):
        print(f"category {i}")
        try:
            response = leboncoin_search(base_url.replace("{cat_id}", str(i)))
        except Exception as e:
            print(f"Request error for category {i}: {e}")
            jump += 1
            if jump >= max_jump:
                print(f"Stopped after {max_jump} consecutive request errors.")
                break
            continue

        try:
            data = json.loads(response.text)
        except Exception as e:
            print(f"Invalid JSON for category {i}: {e}")
            jump += 1
            if jump >= max_jump:
                print(f"Stopped after {max_jump} consecutive invalid JSON responses.")
                break
            continue

        if not data or "ads" not in data or not data["ads"]:
            print(f"No ads found for category {i}")
            jump += 1
            if jump >= max_jump:
                print(f"Stopped after {max_jump} consecutive empty results.")
                break
            continue

        # On a des ads valides : on les ajoute tous à ads_all et on réinitialise jump
        try:
            ads_all.extend(data["ads"])
            jump = 0
        except Exception as e:
            print(f"Error appending ads for category {i}: {e}")
            jump += 1
            if jump >= max_jump:
                print(f"Stopped after {max_jump} consecutive append errors.")
                break

    # Construction de la liste unique des catégories depuis ads_all
    categories_map: Dict[Any, str] = {}
    for ad in ads_all:
        cid = ad.get("category_id")
        cname = ad.get("category_name") or ad.get("category") or f"cat_{cid}"
        if cid is None:
            continue
        # garder la première occurrence si déjà existante
        if cid not in categories_map:
            categories_map[cid] = cname

    for cid, cname in categories_map.items():
        category_list.append({"category_id": cid, "category_name": cname})

    # Optionnel : trier par category_id
    category_list.sort(key=lambda x: (x["category_id"] is None, x["category_id"]))
    return category_list


if __name__ == "__main__":
    """
    categories = get_category_list(max_jump=5, max_cat=200)
    df = pd.DataFrame(categories)

    df.to_excel("output/leboncoin_catagories_with_id.xlsx", index=False)

    print(f"\nExported {len(df)} categories to 'output/leboncoin_catagories_with_id.xlsx'\n")
    print(df)
    """
    search_param = {
        "page": "_page_",
        "category": "_category_",
        "order": "desc",
        "sort": "time",
        "ad_type": "offer"
    }
    search_url = query_builder(**search_param).replace("_page_", str(2)).replace("_category_", str(2))
    