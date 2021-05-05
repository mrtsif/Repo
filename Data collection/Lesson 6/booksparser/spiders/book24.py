import scrapy
from scrapy.http import HtmlResponse
from booksparser.items import BooksparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/catalog/school-1492/']

    def parse(self, response):
        books_links = response.xpath("//div [@class = 'product-card__image-holder']/a/@href").extract()
        next_page = response.xpath("//a[@class = 'pagination__item _link _button _next smartLink']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in books_links:
            yield response.follow(link, callback=self.books_pars)

    def books_pars(self, response: HtmlResponse):
        link = response.url
        name = response.xpath('//h1/text()').extract_first()
        authors = response.xpath("//a[@class = 'item-tab__chars-link' and @itemprop = 'author']/text()").extract()
        old_price = response.xpath("//div[@class = 'item-actions__price-old']/text()").extract_first()
        new_price = response.xpath("//b[@itemprop = 'price']/text()").extract_first()
        rate = response.xpath("//div[@class = 'rating__rate-value _bold']/text()").extract_first()
        yield BooksparserItem(link=link, name=name, authors=authors, old_price=old_price, new_price=new_price,
                              rate=rate)
