# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .db import db,Logo
from peewee import IntegrityError
from .items import LogoExtractorItem
import logging
from selenium import webdriver
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

class LogoExtractorPipeline(object):
    """
    This class will extract the item and push it in the DB.

    """
    def __init__(self):
        """
        Initialize the pipeline.
        """
        self.log = logging.getLogger(__name__)
        self.sanity_check = settings.get("SANITY_CHECK_LOGO_POSITION",False)
        if self.sanity_check:
            self.driver = webdriver.Chrome(
                executable_path=settings["CHROME_WEBDRIVER_PATH"])
            with open(settings.get('JQUERY_LOCATION','js/jquery-3.3.1.min.js'), 'r') as jquery_js:
                self.jquery = jquery_js.read()  # read the jquery from a file

    def process_item(self, item:LogoExtractorItem, spider):
        """
        Process the item and push it into the DB.
        :param item: the LogoExtractorItem that comes from the Spider
        :param spider: the LogoExtractor Spider
        :return:
        """
        self.log.info("processing url: %s" %item['url'])
        # If the item is an image url then push it in the DB.
        if item['is_img']:
            self.log.info("found image : %s" %item['logo_url'])
            # First clean up the URL
            if 'http' in item['logo_url']:
                logo_url = item['logo_url']
            else:
                logo_url = item['url']+"/"+item['logo_url']
            # Push it to DB
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
            # If item is not image URL and is in fact None,
            # This means that image is not found and webpage does not have a logo in the header
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
            #     If item is not image, but in fact is <a> then we try to get the background image
            # by using headless browser
            else:
                # Do we want to use headless browser ?
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
                #   If you don't like to use headless then nothing we can do
                else:
                    try:
                        with db.atomic():
                            Logo.get_or_create(
                                logo_url='ITEM HAS LOGO BUT YOU DON\'T WANT IT',
                                web_url=item['url']
                            )
                        self.log.info("Item have a logo probably but added to DB without the Logo URL ! ")
                    except IntegrityError:
                        pass

        return item
