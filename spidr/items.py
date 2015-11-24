# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpidrItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    avgPrice = scrapy.Field()
    features = scrapy.Field()
