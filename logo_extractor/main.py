
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from selenium import webdriver
import pdfminer
from logo_extractor.db import *



if __name__ == '__main__':
    with open("urls.txt") as urls_file :
        temp = urls_file.readlines()
    urls = [x.split(',')[0] for x in temp]
    #
    # urls = [
    #     "http://ground-truth-data.s3-website-us-east-1.amazonaws.com/autoglassforyou.com",
    #     "http://ground-truth-data.s3-website-us-east-1.amazonaws.com/www.sammiesdoggydaycare.com",
    #     "http://ground-truth-data.s3-website-us-east-1.amazonaws.com/www.reubenm.me",
    #     "http://ground-truth-data.s3-website-us-east-1.amazonaws.com/smileesthetics.com",
    #     "http://ground-truth-data.s3-website-us-east-1.amazonaws.com/catchmyparty.com",
    # ]
    # # driver.get(urls[3])
    # # driver.execute_script(jquery)  # active the jquery lib
    # # loc = driver.execute_script("return $('img[src*=logo]').offset()")
    #
    create_tables()
    db.connect(reuse_if_open=True)
    process = CrawlerProcess(get_project_settings())
    process.crawl('logo',urls=urls)
    process.start()
    db.close()
