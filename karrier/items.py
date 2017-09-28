# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KarrierItem(scrapy.Item):
    name = scrapy.Field()
    place = scrapy.Field()
    url_to_pdf = scrapy.Field()
    text = scrapy.Field()
    einstellung = scrapy.Field()
    additional_text = scrapy.Field()
