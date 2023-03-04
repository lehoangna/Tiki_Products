import pymongo

product_by_category = {}

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myClient["tiki_products"]

products = db.products.find({}, {"productset_group_name": 1, "_id": 0})
products = list(products)

for product in products:
    category_list = product['productset_group_name'].split('/')
    for i in range(0,len(category_list)):
        category = category_list[i]
        if(category=='NGON'): category = 'Tiki Ngon'
        if category in product_by_category:
            product_by_category[category] += 1
        else:
            product_by_category[category] = 1

with open('count_category.txt', 'w', encoding='utf-8') as f:
    for key, value in product_by_category.items():
        f.write(key + ": " + str(value)+'\n')