import csv
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher

class MasterstudiengangSpider(scrapy.Spider):
    name = 'Masterstudiengang'

    def start_requests(self):
        URL = 'https://www.fhnw.ch/de/studium/master"'
        yield scrapy.Request(url=URL, callback=self.response_parser)

    def response_parser(self, response):
        for selector in response.css('article.product_pod'):
            yield {
                'Master_of': selector.css('span.widg_teaser__dateline::text').get(),
                'Studiengang': selector.xpath('.//h3/text()').get(),
                'Link': selector.css('a.widg_teaser__link::attr(href)').get(),
            }

        next_page_link = response.css('li.next a::attr(href)').extract_first()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.response_parser)



def masterstudiengang_spider_result():
    masterstudiengang_results = []

    def crawler_results(item):
        masterstudiengang_results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    crawler_process = CrawlerProcess()
    crawler_process.crawl(MasterstudiengangSpider)
    crawler_process.start()
    return masterstudiengang_results


if __name__ == '__main__':
    masterstudiengang_data=masterstudiengang_spider_result()

    keys = masterstudiengang_data[0].keys()
    with open('masterstudiengang_data.csv', 'w', newline='') as output_file_name:
        writer = csv.DictWriter(output_file_name, keys)
        writer.writeheader()
        writer.writerows(masterstudiengang_data)