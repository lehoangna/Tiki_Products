import time
import requests
import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myClient["tiki_products"]

image_urls = db.products.find({}, {"images.base_url": 1, "_id": 0})
list_image_urls = list(image_urls)

for image in list_image_urls:
    for url in image['images']:
        file_name = url['base_url'].split('/')[-1]
        with open('D:/images_tiki/'+file_name, 'wb') as f:
            f.write(requests.get(url['base_url']).content)
        time.sleep(0.25)