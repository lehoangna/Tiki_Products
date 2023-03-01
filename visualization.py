import pymongo
import pandas as pd
import matplotlib.pyplot as plt

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
    products_df_by_cate = products_df.loc[products_df['categories'] == i, :]
    products_df_by_cate = products_df_by_cate.sort_values(by=['prices'])
    products_df_by_cate = products_df_by_cate.head(50)
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.scatter(products_df_by_cate['prices'], products_df_by_cate['rating'], label='rating', s=25)
    ax2.scatter(products_df_by_cate['prices'], products_df_by_cate['quantity'], color=['red'], label='quantity', s=25)
    ax1.set_xlabel("Price")
    ax1.set_ylabel("Rating")
    ax2.set_ylabel("Quantity")
    plt.legend()
    plt.title(i)
    ax1.legend(loc=0)
plt.show()