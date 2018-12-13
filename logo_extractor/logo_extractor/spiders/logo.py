# -*- coding: utf-8 -*-
import scrapy
from ..items import LogoExtractorItem as logoItem


class LogoSpider(scrapy.Spider):
    name = 'logo'

    def __init__(self,urls=None,*args,**kwargs):
        super(LogoSpider, self).__init__(*args, **kwargs)
        # Check if urls is a list
        # TODO: Check if urls is a str.
        if isinstance(urls,list):
            self.start_urls = urls
        else:
            self.start_urls = list(urls)

    def parse(self, response):
        """
        We parse the webpage naively. We look at 3 cases:
            First, we look at images inside a <div> or <header>
            Second, images that are in a <a> tag or <div> which are part of header or logo
            Third, we look at <a>,<li>,<div> tags that have header in their class or id and have a background image
        :param response: The webpage to be parsed
        :return:
        """
        header = response.xpath("//div[contains(@class,'head') or contains(@id,'head')] | //div[contains(@class,'logo') or contains(@id,'logo')] | //header[contains(@class,'logo') or contains(@id,'logo')] | //header[contains(@class,'head') or contains(@id,'head')]")
        if header is not None:
            if len(header) > 1:
                header = header[0]
        imgs = header.xpath(".//img/@src").extract_first()

        if imgs:
            return logoItem(
                url = response.url,
                logo_url = imgs,
                is_img = True
            )
        header = response.xpath(
            "//div[contains(@class,'head') or contains(@id,'head')] | //div[contains(@class,'logo') or contains(@id,'logo')] | //header[contains(@class,'logo') or contains(@id,'logo')] | //header[contains(@class,'head') or contains(@id,'head')]")
        a_s = header.xpath(".//a[contains(@id,'logo') or contains(@class,'logo') or contains(@name,'logo')]")
        if a_s:
            return logoItem(
                url=response.url,
                logo_url=a_s,
                is_img = False
            )

        return logoItem(url=response.url,logo_url=None,is_img=False)
