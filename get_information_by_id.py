import time
import requests
import pymongo
from crawl_data import products_id
# id = ['11756216', '198350840']
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
}
myClient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myClient["tiki_products"]

for i in products_id:
    # try:
    response = requests.get('https://tiki.vn/api/v2/products/' + str(i), headers=HEADERS)
    # except requests.exceptions.RequestException as e:  # This is the correct syntax
    #     raise print('123'+e)
    print(response.status_code)
    json = response.json()
    db.products.insert_one(json)
    time.sleep(0.25)