
    import csv
    import scrapy
    from scrapy import signals
    from scrapy.crawler import CrawlerProcess
    from scrapy.signalmanager import dispatcher

    class masterstudiengangSpider(scrapy.Spider):
        name = 'masterstudiengang'

        def start_requests(self):
            URL = 'https://www.zhaw.ch/de/studium/masterstudiengaenge/'
            yield scrapy.Request(url=URL, callback=self.response_parser)

        def response_parser(self, response):
            for selector in response.css('article.product_pod'):                        # hier anpassen
                yield {
                    'title': selector.css('h3 > a::attr(title)').extract_first(),       # hier anpassen
                    'price': selector.css('.price_color::text').extract_first()         # hier anpassen
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
        crawler_process.crawl(masterstudiengangSpider)
        crawler_process.start()
        return masterstudiengang_results

    if __name__ == '__main__':
        masterstudiengang_data = masterstudiengang_spider_result()

        keys = masterstudiengang_data[0].keys()
        with open('masterstudiengang_data.csv', 'w', newline='') as output_file_name:
            writer = csv.DictWriter(output_file_name, keys)
            writer.writeheader()
            writer.writerows(masterstudiengang_data)