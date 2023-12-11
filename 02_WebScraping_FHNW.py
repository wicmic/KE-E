import scrapy


class MasterstudiengangSpider(scrapy.Spider):
    name = "masterstudiengang"
    allowed_domains = ["www.fhnw.ch"]
    start_urls = ["https://www.fhnw.ch/de/studium/master"]

    def parse(self, response):
        Master_of = response.css('span.widg_teaser__dateline::text').getall()
        Studiengang = response.xpath('//h3/text()').getall()
        Link = response.css('a.widg_teaser__link::attr(href)').getall()

        yield {
            'Master of':Master_of,
            'Studiengang':Studiengang,
            'Link':Link
        }

