# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NambaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    cafe_name = scrapy.Field()
    cafe_image_url = scrapy.Field()
    cafe_background_image_url = scrapy.Field()
    average_price = scrapy.Field()
    delivery_price = scrapy.Field()
    working_hours = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    categories = scrapy.Field()
    reviews = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    parent_categories = scrapy.Field()


