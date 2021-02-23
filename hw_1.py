from pathlib import Path
import requests
import time
import json

class Parse5ka:
    headers = {
        'Accept': 'application/json',
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
    }

    def __init__(self, start_url, products_path):
        self.start_url = start_url
        self.products_path = products_path

    def _get_response(self, url):
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def run(self):
        for product in self.parse(self.start_url):
            product_path = self.products_path.joinpath(f"f{product['id']}.json")
            self._save(product, product_path)

    def _parse(self, url):
        while url:
            response = self._get_response(url)
            data = response.json()
            url = data['next']
            for product in data['results']:
                yield product

    @staticmethod
    def _save(data, file_path):
        file_path.write_text(json.dumps(data), encoding='UTF-8')

class CategoriesParser(Parse5ka):

    def __init__(self, categories_url, *args, **kwargs):
        self.categories_url = categories_url
        super().__init__(*args, **kwargs)

    def _get_categories(self, ):
        response = self._get_response(self.categories_url)
        data = response.json()
        return data

    def run(self):
        for category in self._get_categories():
            category['products'] = []
            url = f"{self.start_url}?categories={category['parent_group_code']}"
            file_path = self.products_path.joinpath(f"{category['parent_group_code']}.json")
            category['products'].extend(list(self._parse(url)))
            self._save(category, file_path)

def get_dir_path(dirname):
    dir_path = Path(__file__).parent.joinpath(dirname)
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path

if __name__ == '__main__':
    url = 'https://5ka.ru/api/v2/special_offers'
    product_path = get_dir_path('products')
    cat_path = get_dir_path('category')
    cat_url = 'https://5ka.ru/api/v2/categories/'
    cat_parser = CategoriesParser(cat_url, url, cat_path)
    cat_parser.run()