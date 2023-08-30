import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

URL = 'http://books.toscrape.com'


def main():
    book_uris = []
    book_data = []

    # get book urls
    print("Retrieve URLs ...")
    for i in tqdm(range(1, 2)): ## change to while True and catch 404s and other errors
        page_url = URL + f'/catalogue/page-{i}.html'
        response = requests.get(page_url)

        if response.status_code == 404:
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.findAll('article', {'class': 'product_pod'})

        for book in books:
            book_uri = book.find('a')
            book_uris.append(book_uri['href'])

    # scrape individual pages
    print("Scrape book pages ...")
    for book_uri in tqdm(book_uris):
        book_url = URL + '/catalogue/' + book_uri
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

        description = soup.findAll('p')[-1].text

        book_data.append({
            'title': title,
            'price': price,
            'availability': availability,
            'upc': upc,
            'description': description
        })

        break

    book_data = pd.DataFrame(book_data)
    print(book_data.head())


if __name__ == '__main__':
    main()
