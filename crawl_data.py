from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import json

FIRST_PAGE = 1
LAST_PAGE = 51

categories = []
products_id = []

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
}

def getCategory():
    page = 'https://tiki.vn'
    # html = urlopen(page)
    # soup = BeautifulSoup(html.read(), 'html.parser')
    result = requests.get(page, headers=HEADERS)
    source = result.text
    soup = BeautifulSoup(source, 'html.parser')
    category_cards = soup.find_all('div', class_='styles__FooterSubheading-sc-32ws10-5 cNJLWI')

    for i in range(len(category_cards)):
        if(i==1): continue
        category_url = category_cards[i].select('a')[0].attrs['href']
        categories.append(category_url.partition('/c')[2])

def getProductInOnePage(category_link, pagination):
    pagination = str(pagination)
    page = 'https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&include=advertisement&aggregations=2&trackity_id=9f0706eb-cddc-44cf-3333-67df659d9c40&category='+category_link+'&page='+pagination
    # html = urlopen(page)
    # soup = BeautifulSoup(html.read(), 'html.parser')
    response = requests.get(page, headers=HEADERS)
    json = response.json()
    data = json['data']

    for i in range(len(data)):
        products_id.append(data[i]['id'])

getCategory()
for category in categories:
    for i in range(FIRST_PAGE, LAST_PAGE):
        getProductInOnePage(category, i)

# for i in range(1, 6):
#     getProductInOnePage('2549', i)

print(len(products_id))
