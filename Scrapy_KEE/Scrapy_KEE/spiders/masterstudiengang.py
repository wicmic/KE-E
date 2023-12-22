import scrapy
import pandas as pd

class MasterstudiengangSpider(scrapy.Spider):
    name = "masterstudiengang"
    allowed_domains = ["www.fhnw.ch"]
    start_urls = ["https://www.fhnw.ch/de/studium/master"]

    def parse(self, response):
        Master_of = response.css('span.widg_teaser__dateline::text').getall()
        Studiengang = response.xpath('//h3/text()').getall()
        Link = response.css('a.widg_teaser__link::attr(href)').getall()


        # Daten als csv speichern
        data = [{'Master of': m, 'Studiengang': s, 'Link': l} for m, s, l in zip(Master_of, Studiengang, Link)]
        df = pd.DataFrame(data)
        df.to_csv('masterstudiengang_base_fhnw.csv')



# Vorgehen starten im Terminal:
# 1. cd "D:\Python\KE-E\Scrapy_KEE\Scrapy_KEE"
# 2. d:
# 3. scrapy crawl masterstudiengang


# Check im Terminal:
# 1. cd "D:\Python\KE-E\Scrapy_KEE\Scrapy_KEE"
# 2. d:
# 3. scrapy shell
# 4. r = scrapy.Request(url='https://www.fhnw.ch/de/studium/master')        (Link ändern)
# 5. fetch(r)
# 6. response.body
# 7. response.xpath('//h3/text()').getall()     (hier in Klammer anpassen, je nach xpath vom Element)

