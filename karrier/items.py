# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KarrierItem(scrapy.Item):
    name = scrapy.Field()
    url_to_pdf = scrapy.Field()
    date = scrapy.Field()
    address = scrapy.Field()
    stellenumfang = scrapy.Field()
    platze = scrapy.Field()
    befristung = scrapy.Field()
