# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 17:44:28 2025

@author: Lenovo
--------------------------------------------------------------------
FILTER AND QUERY BUILDER

sort 
    default : sort by relevance
    time    : most recent first
    price   : most expensive
   
order
    asc     : Ascendant
    desc    : Descendant
    
ad_type 
    offer   : by default
    demand  : 

owner_type
    private : 
    pro     : professionnel 

urgent : 1 if urgent, else None

sample query
    https://www.leboncoin.fr/recherche?category=1&ad_type=demand&urgent=1&owner_type=pro&sort=price&order=desc
"""

"""
CATEGORIES CATALOGUE :
    1 : vehicule
"""

from bs4 import BeautifulSoup 
import json
from typing import List, Dict, Any
from script.piloterr import leboncoin_search
import pandas as pd

def get_category_list_from_all_ads(max_jump: int = 5, max_cat: int = 100) -> List[Dict[str, Any]]:
    """
    Parcourt les catégories de 1 à max_cat, agrège toutes les annonces renvoyées
    (ads) dans une liste `ads_all`. Si on rencontre max_jump réponses consécutives
    invalides/vides on arrête. À la fin, on extrait les catégories uniques
    (category_id + category_name) depuis ads_all.
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


def query_builder():
    """À implémenter plus tard"""
    return None


def is_404_page(html: str) -> bool:
    soup = BeautifulSoup(html, "html.parser")  
    page_404 = soup.find("h1")

    if page_404 and "404" in page_404.text:
        return True
    return False


def get_category_list(max_jump: int = 5):
    """
    Loop over categories until a 404 page or max_jump consecutive invalid responses.
    """
    base_url = "https://www.leboncoin.fr/recherche?category={cat_id}"

    category_list = []
    jump = 0  # Compte les échecs consécutifs

    print("Scraping leboncoin categories with IDs")

    for i in range(1, 100):
        print(f"category {i}")
        response = leboncoin_search(base_url.replace("{cat_id}", str(i)))

        try:
            data = json.loads(response.text)
        except Exception as e:
            print(f"Invalid JSON for category {i}: {e}")
            jump += 1
            if jump >= max_jump:
                print(f"Stopped after {max_jump} consecutive invalid responses.")
                break
            continue

        if data is None or "ads" not in data or len(data["ads"]) == 0:
            print(f"No ads found for category {i}")
            jump += 1
            if jump >= max_jump:
                print(f"Stopped after {max_jump} consecutive empty results.")
                break
            continue

        try:
            ads_instance = data["ads"][0]
            category_list.append({
                "category_id": ads_instance.get("category_id", i),
                "category_name": ads_instance.get("category_name", f"cat_{i}")
            })
            jump = 0  # ✅ reset dès qu’on trouve une réponse valide

        except Exception as e:
            print(f"Unexpected error for category {i}: {e}")
            jump += 1
            if jump >= max_jump:
                print(f"Stopped after {max_jump} consecutive exceptions.")
                break

    return category_list


if __name__ == "__main__":
    # scrape and export categories with id's
    """
    categories = get_category_list()
    df = pd.DataFrame(categories)
    df.to_excel("output/leboncoin_catagories_with_id.xlsx")
    
    print(df)
    """
    categories = get_category_list_from_all_ads(max_jump=5, max_cat=200)
    df = pd.DataFrame(categories)

    df.to_excel("output/leboncoin_catagories_with_id.xlsx", index=False)

    print(f"\nExported {len(df)} categories to 'output/leboncoin_catagories_with_id.xlsx'\n")
    print(df)
    