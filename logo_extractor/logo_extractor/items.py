# -*- coding: utf-8 -*-
import scrapy


class LogoExtractorItem(scrapy.Item):
    """"
    Defines the list of fields for items extracted from the webpage
    url : the url of the website
    logo_url : the logo URL for the website
    is_img : is the item an image or a <a>
    """
    url = scrapy.Field()
    logo_url = scrapy.Field()
    is_img = scrapy.Field()

