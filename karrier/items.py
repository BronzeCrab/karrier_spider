# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KarrierItem(scrapy.Item):
    name = scrapy.Field()
    einstellungsdatum = scrapy.Field()
    address = scrapy.Field()
    stellenumfang = scrapy.Field()
    platze = scrapy.Field()
    befristung = scrapy.Field()
    besoldungs = scrapy.Field()
    stellennummer = scrapy.Field()
    url_to_pdf = scrapy.Field()
    text = scrapy.Field()
    place = scrapy.Field()
    additional_text = scrapy.Field()
    detailed_data = scrapy.Field()
