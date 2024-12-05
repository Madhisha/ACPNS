# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CgpaItem(scrapy.Item):
    roll_no = scrapy.Field()
    result_table = scrapy.Field()
    cgpa = scrapy.Field()
