from pathlib import Path
import requests
import bs4
import time
import json

class MagnitParse:

    data_temlate = {
        'url': "",
        'promo_name': "",
        'title': "",
    }
    def __init__(self, start_url):
        self.start_url = start_url

    def _get_response(self, url):
        response = requests.get(url)
        return response

    def _get_soup(self, url):
        response = self._get_response(url)
        soup = bs4.BeautifulSoup(response.text, "lxml")
        return soup

    def run(self):
        soup = self._get_soup(self.start_url)
        catalog = soup.find('div', attrs={'class': 'catalogue__main'})
        for product_a in catalog.find_all('a', recursive=False):
            product_data = self._parse(product_a)
            print(1)

    def _parse(self, produkt_a:bs4.Tag):
        print(1)

    def save(self, data, ):
        pass