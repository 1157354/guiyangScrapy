# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GuiyangscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    data_field = scrapy.Field()
    abstract = scrapy.Field()
    keyword = scrapy.Field()
    theme_classification = scrapy.Field()
    industry_classfication = scrapy.Field()
    service_classfication = scrapy.Field()
    open_attribute = scrapy.Field()
    update_frequency = scrapy.Field()
    release_date = scrapy.Field()
    update_date = scrapy.Field()
    data_supplier_agent = scrapy.Field()
    data_supplier_address = scrapy.Field()
    data_maintenance_agent = scrapy.Field()
    language = scrapy.Field()
    file_size = scrapy.Field()
    file_amount = scrapy.Field()
    record_size = scrapy.Field()
    security_degree = scrapy.Field()
    resId = scrapy.Field()
    file_name = scrapy.Field()


