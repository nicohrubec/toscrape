from src.scrapers.BooksScraper import BooksScraper

URL = 'http://books.toscrape.com'


def main():
    bs = BooksScraper()
    data = bs.scrape()
    print(data.head())

if __name__ == '__main__':
    main()
