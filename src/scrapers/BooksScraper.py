import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


class BooksScraper:
    URL = 'http://books.toscrape.com'

    def _get_uris(self):
        book_uris = []

        print("Retrieve URLs ...")
        for i in tqdm(range(1, 3)):
            page_url = self.URL + f'/catalogue/page-{i}.html'
            response = requests.get(page_url)

            if response.status_code == 404:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            books = soup.findAll('article', {'class': 'product_pod'})

            for book in books:
                book_uri = book.find('a')
                book_uris.append(book_uri['href'])

        return book_uris

    def _scrape_uri(self, uri):
        book_url = self.URL + '/catalogue/' + uri
        response = requests.get(book_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        book_info = soup.find('div', {'class': 'product_main'})

        title = book_info.find('h1').text.strip()
        price = book_info.find('p', {'class': 'price_color'}).text.strip()[1:]
        availability = book_info.find('p', {'class': 'instock availability'}).text.strip()

        info_table = soup.find('table')

        upc = '-'
        for row in info_table.findAll('tr'):
            if row.find('th').text.strip() == 'UPC':
                upc = row.find('td').text

        return {
            'title': title,
            'price': price,
            'availability': availability,
            'upc': upc
        }

    def scrape(self):
        book_data = []
        book_uris = self._get_uris()

        for book_uri in tqdm(book_uris):
            book_entry = self._scrape_uri(book_uri)
            book_data.append(book_entry)

        book_data = pd.DataFrame(book_data)
        return book_data
