# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 19:44:47 2025

@author: Lenovo
"""

from script.piloterr import leboncoin_search
from utils.leboncoin import query_builder
import json

#search_string = "https://www.leboncoin.fr/recherche?category=9"
#search_string = "https://www.leboncoin.fr/recherche?category=33&jobfield=10&page=2"

"""
search_string = "https://www.leboncoin.fr/recherche?category=1"
response = leboncoin_search(search_string)
result = json.loads(response.text)
"""

search_string = query_builder(page="2",category="2",order="desc",sort="price")
response = leboncoin_search(search_string)
result = json.loads(response.text)