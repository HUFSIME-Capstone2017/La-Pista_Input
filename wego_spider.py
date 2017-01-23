import scrapy
from selenium import webdriver
import time
from scrapy.selector import Selector

from wego.items import WegoItem

class WegoSpider(scrapy.Spider):
    name = "wego"
    allowed_domains = ["jetradar.com"]
    start_urls = ["http://www.jetradar.com/searches/CSEL2401CPARY1"]

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome("/Users/ERRERO/chromedriver")

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(20)

        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)
        rows = selector.xpath('//*[@id="results_add_container"]/div[7]/div')

        for row in rows:
            item = WegoItem()
            item["price"] = row.xpath('./div/div/div[1]/a/div/span/text()')[0].extract()
            item["dep_F"] = row.xpath('./div/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/span[1]/text()')[0].extract()
            item["dep_P"] = row.xpath('./div/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/span[2]/text()')[0].extract()
            item["dep_APM"] = row.xpath('./div/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div[2]/p[1]/text()')[0].extract()
            item["dep_T"] = row.xpath('./div/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div[1]/text()')[0].extract()
            item["dep_date"] = row.xpath('./div/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div[2]/p[2]/text()')[0].extract()
            item["stop_N"] = row.xpath('./div/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/text()')[0].extract()
            item["duration"] = row.xpath('./div/div/div[2]/div[1]/div[2]/div/div[2]/div[3]/text()')[0].extract()
            item["arr_F"] = row.xpath('./div/div/div[2]/div[1]/div[2]/div/div[3]/div[1]/span[2]/text()')[0].extract()
            item["arr_P"] = row.xpath('./div/div/div[2]/div[1]/div[2]/div/div[3]/div[1]/span[1]/text()')[0].extract()
            item["arr_APM"] = row.xpath('./div/div/div[2]/div[1]/div[2]/div/div[3]/div[2]/div[1]/div[1]/text()')[0].extract()
            item["arr_T"] = row.xpath('./div/div/div[2]/div[1]/div[2]/div/div[3]/div[2]/div[2]/text()')[0].extract()
            item["arr_date"] = row.xpath('./div/div/div[2]/div[1]/div[2]/div/div[3]/div[2]/div[1]/div[2]/text()')[0].extract()
            yield item

        dep = ['ICN', 'PAR']

        for a in dep:
            for b in dep:
                if a != b:
                    for month in range(2, 5):
                        for day in range(1, 32):
                            if day < 10:
                                day = "0" + str(day)
                                next_page = "http://www.jetradar.com/searches/A" + a + str(day) + "0" + str(month) + "A" + b + "Y1"
                            elif day == day:
                                next_page = "http://www.jetradar.com/searches/A" + a + str(day) + "0" + str(month) + "A" + b + "Y1"
                            yield scrapy.Request(next_page, callback=self.parse)