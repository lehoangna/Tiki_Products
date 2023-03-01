import pymongo

product_by_category = {}

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myClient["tiki_products"]

products = db.products.find({}, {"productset_group_name": 1, "_id": 0})
products = list(products)

for product in products:
    category = product['productset_group_name'].split('/')[-1]
    if category in product_by_category:
        product_by_category[category] += 1
    else:
        product_by_category[category] = 1

# print(product_by_category)