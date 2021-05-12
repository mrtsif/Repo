import scrapy
from scrapy.http import HtmlResponse
from bmparser.items import BmparserItem
from scrapy.loader import ItemLoader


class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/kuhni/']

    def parse(self, response:HtmlResponse):
        positions_links = response.xpath("//a[@class = 'bex6mjh_plp b1f5t594_plp iypgduq_plp nf842wf_plp']/@href").extract()
        for link in positions_links:
            yield response.follow(link, callback=self.lerua_parse)


    def lerua_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=BmparserItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('characteristics', "//div[@class = 'def-list__group']/*/text()")
        loader.add_xpath('price', "//span[@slot = 'price']/text()")
        loader.add_xpath('photos', "//img[@slot = 'thumbs']/@src")
        yield loader.load_item()