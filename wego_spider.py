import scrapy
from selenium import webdriver
import time
from scrapy.selector import Selector

from wego.items import WegoItem

class WegorSpider(scrapy.Spider) :
    name = "wego"
    allowed_domains = ["wego.co.kr"]
    start_urls = [
        "https://www.wego.co.kr/en/flights/search/79W3L-OVTVqlVGtXxGu80A?relative_comfort_index=-150&outbound_date=2017-01-20&departure_code=SEL&arrival_code=PAR&cabin=economy"
        ]

    def __init__(self) :
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome("/Users/ERRERO/chromedriver")

    def parse(self, response) :
        self.browser.get(response.url)
        time.sleep(20)

        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)
        rows = selector.xpath('//*[@id="container"]/div[3]/div[7]/div[3]/div[2]/div/div/div[3]/div[2]/section')

        for row in rows :
            item = WegoItem()
            item["departure"] = row.xpath('./div[1]/div[1]/div[1]/div[2]/div[1]/span[1]/text()')[0].extract
            item["destination"] = row.xpath('./div[1]/div[1]/div[1]/div[2]/div[1]/span[2]/text()')[0].extract
            yield item