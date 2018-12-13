# -*- coding: utf-8 -*-
import scrapy


class LogoExtractorItem(scrapy.Item):
    # Defines the list of fields for items extracted from the webpage
    title = scrapy.Field()
    url = scrapy.Field()
    logo_url = scrapy.Field()
    is_img = scrapy.Field()

