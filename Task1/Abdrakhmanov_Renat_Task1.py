import requests
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm
import os
from urllib.parse import quote_plus
import pandas as pd

url = 'https://kingfisher.kz'
req = requests.get(url)
soup = BeautifulSoup(req.content, 'lxml')

city_address_list = []
product_list = []

for product in tqdm(soup.find('ul', {'class':'topMenu'}).find_all('li',{'class':'dropmenu'})):
    product_list.append(product.find('a')['href'][:(product.find('a')['href'][1:].find('/')+1)])

for city in tqdm(soup.find('div', {'id':'popupSelCity'}).find_all('a', {'href': lambda n: n and 'city' in n})):
    response = session.get('https://kingfisher.kz' + city['href'])
    city_address_list.append(session.cookies.get_dict()['city_select'])


product_titles = []
product_categories = []
product_prices = []
product_cities = []
product_availabilities = []

for city_address in tqdm(city_address_list):
    for product in tqdm(product_list):
        url = 'https://kingfisher.kz' + product
        page = requests.post(url, cookies={'city_select': city_address})
        soup = BeautifulSoup(page.text, 'lxml')
        
        for item in soup.find_all('div', {'class':'goodsBlock'}):
            product_titles.append(item.find('span', {'class':'wrapperPad'}).find('a', {'class':'title'}).find('span').get_text().strip())
            product_categories.append(soup.find('div', {'class':'Goods goodslist padSpace'}).find('h1', {'class':'title'}).get_text().strip())
            product_prices.append(item.find('span', {'class':'wrapperPad'}).find('span', {'class':'price'}).find('span', {'class':'new'}).get_text().strip())
            product_cities.append(soup.find('div', {'class':'wrapperLeft'}).find('span').get_text())
            try:
                product_availabilities.append(item.find('span', {'class':'wrapperPad'}).find('span', {'class':'wrapperNone'}).find('span', {'class':'None'}).get_text().strip())
            except:
                product_availabilities.append('В наличии')
            
        
result = list(zip(product_titles, product_categories, product_prices, product_cities, product_availabilities))

df = pd.DataFrame(result, columns = ['Title', 'Category', 'Price', 'City', 'Availability'])

df.to_csv('Abdrakhmanov_Renat_Task1.csv')