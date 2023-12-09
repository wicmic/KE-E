import scrapy


class MasterstudiengangSpider(scrapy.Spider):
    name = "masterstudiengang"
    allowed_domains = ["www.zhaw.ch"]
    start_urls = ["https://www.zhaw.ch/de/studium/masterstudiengaenge/"]

    def parse(self, response):
        pass
