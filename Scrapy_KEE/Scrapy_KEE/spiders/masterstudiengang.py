import scrapy


class MasterstudiengangSpider(scrapy.Spider):
    name = "masterstudiengang"
    allowed_domains = ["www.fhnw.ch"]
    start_urls = ["https://www.fhnw.ch/de/studium/master"]

    def parse(self, response):
        rows = response.xpath('/div')

        for row in rows:
            #Master_of = row.css('span.widg_teaser__dateline::text').getall()
            Studiengang = row.xpath('.//h3/text()').get()
            # Element 1:     /html/body/div[1]/div[2]/div[2]/div[1]/div[3]/div/div/div/div/div[2]/h3
            # Element 2:    /html/body/div[1]/div[2]/div[2]/div[1]/div[4]/div/div/div/div[2]/div[2]/h3

            #Link = response.css('a.widg_teaser__link::attr(href)').getall()

            yield {
                #'Master of':Master_of,
                'Studiengang':Studiengang,
                #'Link':Link
            }

# 1. Terminal cd "aktuelle Spider" (wo diese py-Datei liegt)
# 2. scrapy crawl masterstudiengang -o masterstudiengang_1.csv