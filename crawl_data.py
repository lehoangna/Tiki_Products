import http
from requests.exceptions import ChunkedEncodingError
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import requests

FIRST_PAGE = 1

categories = []
products_id = []

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
}

def getCategory():
    page = 'https://tiki.vn'
    result = requests.get(page, headers=HEADERS)
    source = result.text
    soup = BeautifulSoup(source, 'html.parser')
    category_cards = soup.find_all('div', class_='styles__FooterSubheading-sc-32ws10-5 cNJLWI')

    for i in range(len(category_cards)):
        if(i==1): continue
        category_url = category_cards[i].select('a')[0].attrs['href']
        categories.append(category_url.partition('/c')[2])

def getCategoryMarket():
    page = 'https://tiki.vn/di-cho-online'
    result = requests.get(page, headers=HEADERS)
    source = result.text
    soup = BeautifulSoup(source, 'html.parser')
    item_count = 1
    for item in soup.select("a[href^='https://tiki.vn/tikingon/']"):
        if(item_count <= 8):
            categories.append(item['href'].split('/')[-1][1:])
        else:
            break
        item_count+=1

# get 40 products in one page of any category
def getProductInOnePage(category_link, pagination):
    pagination = str(pagination)
    page = 'https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&include=advertisement&aggregations=2&trackity_id=9f0706eb-cddc-44cf-3333-67df659d9c40&category='+category_link+'&page='+pagination
    with requests.get(page, headers=HEADERS) as response:
    # response = requests.get(page, headers=HEADERS)
        json = response.json()
        print(pagination)
        if('data' in json):
            data = json['data']
            for i in range(len(data)):
                products_id.append(data[i]['id'])

getCategory()
getCategoryMarket()

# loop through all category that can handle
for category in categories:
    page = 'https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&include=advertisement&aggregations=2&trackity_id=9f0706eb-cddc-44cf-3333-67df659d9c40&category=' + category + '&page=1'
    with requests.get(page, headers=HEADERS) as response:
    # response = requests.get(page, headers=HEADERS)
        json = response.json()
        print(category)
        category_paging = json['paging']
        last_page = category_paging['last_page']
        for i in range(FIRST_PAGE, last_page+1):
            try:
                getProductInOnePage(category, i)
            except ChunkedEncodingError as e:
                continue
            except ConnectionError as e:
                continue
            except http.client.IncompleteRead as e:
                continue


print(len(products_id))