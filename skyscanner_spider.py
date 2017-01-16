import scrapy
from selenium import webdriver
import time
from scrapy.selector import Selector

from skyscanner.items import SkyscannerItem

class SkyscannerSpider(scrapy.Spider) :
    name = "skyscanner"
    allowed_domains = ["skyscanner.co.kr"]
    start_urls = [
        "https://www.skyscanner.co.kr/transport/flights/sela/pari/170120/airfares-from-seoul-to-paris-in-january-2017.html?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=0&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home&seo_airline=ak#results"
        ]

    def __init__(self) :
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome("/Users/ERRERO/chromedriver")

    def parse(self, response) :
        self.browser.get(response.url)
        time.sleep(5) #인위적으로 5초를 줌. 이 과정이없으면 우리가 원하는 결과물을 얻을 수 없음. 결과값이 바로 나오지 않기 때문

        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)
        rows = selector.xpath()

        for row in rows :
            item = SkyscannerItem()
            item["departure"] = row.xpath()[0].extract
            item["destination"] = row.xpath()[0].extract
            yield item