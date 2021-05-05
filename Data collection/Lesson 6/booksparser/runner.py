from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from booksparser import settings
from booksparser.spiders.book24 import Book24Spider
from booksparser.spiders.labirint import LabirintSpider

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(Book24Spider)
    process.crawl(LabirintSpider)

    process.start()