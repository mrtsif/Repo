# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose

def process_photo_links(photo_url):
    correct_url = photo_url.replace(',w_82,h_82,', ',w_2000,h_2000,')
    return correct_url

def process_characteristics(characteristics):
    new_char = {}
    char_list = []
    a = 0
    for i in characteristics:
        i = i.replace(" ", '').replace('\n', '')
        char_list.append(i)
        if a % 2 == 1:
            new_char[char_list[a-1]] = i
        a += 1
    return new_char

def process_prices(price):
    price = ''.join(price)
    price = price.replace(' ', '')
    price = int(price)
    return price


class BmparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field()
    characteristics = scrapy.Field(input_processor=Compose(process_characteristics), output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=Compose(process_prices))
    photos = scrapy.Field(input_processor=MapCompose(process_photo_links))
    _id = scrapy.Field()

