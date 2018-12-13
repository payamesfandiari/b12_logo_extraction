# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .db import db,Logo
from peewee import IntegrityError
from .items import LogoExtractorItem
from scrapy.conf import settings
import logging
from selenium import webdriver


class LogoExtractorPipeline(object):
    def __init__(self):

        self.log = logging.getLogger(__name__)
        self.sanity_check = settings.get("SANITY_CHECK_LOGO_POSITION",False)
        self.driver = webdriver.Chrome(
            executable_path=settings["CHROME_WEBDRIVER_PATH"])
        with open('js/jquery-3.3.1.min.js', 'r') as jquery_js:
            self.jquery = jquery_js.read()  # read the jquery from a file

    def process_item(self, item:LogoExtractorItem, spider):

        self.log.info("processing url: %s" %item['url'])
        if item['is_img']:
            self.log.info("found image : %s" %item['logo_url'])
            if 'http' in item['logo_url']:
                logo_url = item['logo_url']
            else:
                logo_url = item['url']+"/"+item['logo_url']

            try:
                with db.atomic():
                    Logo.get_or_create(
                        logo_url=logo_url,
                        web_url=item['url']
                    )
                self.log.info("Item added to the DB!")
            except IntegrityError:
                pass
        else:
            if item['logo_url'] is None:
                try:
                    with db.atomic():
                        Logo.get_or_create(
                            logo_url='',
                            web_url=item['url']
                        )
                    self.log.info("Item added to the DB without the Logo URL ! ")
                except IntegrityError:
                    pass
            else:
                if self.sanity_check:
                    self.driver.get(item['url'])
                    self.driver.execute_script(self.jquery)  # active the jquery lib
                    a = item['logo_url']
                    a_id = a.xpath('@id').get()
                    a_class = a.xpath('@class').get()
                    if a_id:
                        imgs = self.driver.execute_script("return $('a#{0}').map(function(){{return $(this).css('background-image')!= 'none' ? $(this).css('background-image') : null}})".format(a_id))
                        if len(imgs) == 0 :
                            imgs = self.driver.execute_script(
                                "return $('a#{0}').find('*').map(function(){{return $(this).css('background-image')!= 'none' ? $(this).css('background-image') : null}})".format(
                                    a_id))
                    elif a_class:
                        imgs = self.driver.execute_script("return $('a.{0}').map(function(){{return $(this).css('background-image')!= 'none' ? $(this).css('background-image') : null}})".format(a_class))
                        if len(imgs) == 0 :
                            imgs = self.driver.execute_script(
                                "return $('a.{0}').find('*').map(function(){{return $(this).css('background-image')!= 'none' ? $(this).css('background-image') : null}})".format(
                                    a_class))
                    if len(imgs) > 0:
                        img_url = imgs[0]
                        if img_url.startswith('url('):
                            img_url = img_url[5:-2]

                        if 'http' in img_url:
                            logo_url = img_url
                        else:
                            logo_url = item['url'] + "/" + img_url

                        try:
                            with db.atomic():
                                Logo.get_or_create(
                                    logo_url=logo_url,
                                    web_url=item['url']
                                )
                            self.log.info("Item added to the DB!")
                        except IntegrityError:
                            pass

        return item
