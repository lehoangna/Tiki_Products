import http
import time
import requests
import pymongo
from requests.exceptions import ChunkedEncodingError
from requests.exceptions import ConnectionError
from crawl_data import products_id

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
}
myClient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myClient["tiki_products"]
products_list = []

for i in products_id:
    try:
        with requests.get('https://tiki.vn/api/v2/products/' + str(i), headers=HEADERS) as response:
        # response = requests.get('https://tiki.vn/api/v2/products/' + str(i), headers=HEADERS)
            print(response.status_code)
            json = response.json()
            products_list.append(json)
            # db.products.insert_one(json)
        time.sleep(0.5)
    except ChunkedEncodingError as e:
        continue
    except ConnectionError as e:
        continue
    except http.client.IncompleteRead as e:
        continue
db.products.insert_many(products_list)
print(len(products_list))
print("Done")