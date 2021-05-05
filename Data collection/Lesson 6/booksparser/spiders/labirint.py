import scrapy
from scrapy.http import HtmlResponse
from booksparser.items import BooksparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/genres/11/']

    def parse(self, response: HtmlResponse):
        books_links = response.xpath("//div[@class = 'catalog-responsive outer-catalog catalog']//\
                                     a[@class = 'product-title-link']/@href").extract()
        next_page = response.xpath(
            "//div[@class = 'pagination-next']/a[@class = 'pagination-next__text']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in books_links:
            yield response.follow(link, callback=self.books_pars)

    def books_pars(self, response: HtmlResponse):
        link = response.url
        name = response.css('h1::text').extract_first()
        authors = response.xpath("//div[@class= 'authors']/a[@class = 'analytics-click-js']/text()").extract()
        old_price = response.xpath("//span[@class= 'buying-priceold-val-number']/text()").extract_first()
        new_price = response.xpath("//span[@class= 'buying-pricenew-val-number']/text()").extract_first()
        rate = response.xpath("//div[@id = 'rate']/text()").extract_first()
        yield BooksparserItem(link=link, name=name, authors=authors, old_price=old_price, new_price=new_price,
                              rate=rate)
