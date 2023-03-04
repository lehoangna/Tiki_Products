import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import click
import numpy as np

categories_no_duplicates = []
categories = []
prices = []
rating = []
quantity = []

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myClient["tiki_products"]

products = db.products.find({}, {"price": 1, "rating_average": 1, "all_time_quantity_sold": 1, "productset_group_name": 1, "_id": 0})
products = list(products)

for product in products:
    price = product['price']
    rating_average = product['rating_average']
    quantity_sold = 0
    if "all_time_quantity_sold" in product: quantity_sold = product['all_time_quantity_sold']
    category = product['productset_group_name'].split('/')[0]

    categories.append(category)
    prices.append(price)
    rating.append(rating_average)
    quantity.append(quantity_sold)
    if category not in categories_no_duplicates:
        categories_no_duplicates.append(category)

prd = {
    "categories": categories,
    "prices": prices,
    "rating": rating,
    "quantity": quantity
}
products_df = pd.DataFrame(prd)

for i in categories_no_duplicates:
    products_df['round_price'] = (np.round(products_df['prices'] / 100000) * 100000).astype(int)
    temp = products_df.loc[products_df['categories'] == i]
    re = temp.groupby('round_price', as_index=False)['quantity', 'rating'].mean()

    plt.figure(figsize=(10, 6))
    plt.plot(re['round_price'], re['quantity'])
    plt.plot(re['round_price'], re['rating'] * 100)
    plt.legend(['Quantity', 'Rating 100:1'], fontsize=20)
    plt.grid(True)
    plt.title(i, fontsize=20)
    plt.xlabel('price(milion)', fontsize=14)
    plt.show()
    if click.confirm('Do you want to continue?', default=True):
        plt.close()
    else:
        plt.close()
        break