import scrapy
import pandas as pd

class Masterstudiengang_FHGRSpider(scrapy.Spider):
    name = "masterstudiengang_fhgr"
    allowed_domains = ["www.fhgr.ch"]
    start_urls = ["https://www.fhgr.ch/studium/masterangebot"]

    def parse(self, response):
        Master_of = response.xpath('//div/text()').getall()
        Studiengang = response.xpath('//h4/text()').getall()
        Link = response.xpath('.StudyPath--ContentBox a::attr(href)').getall()

        # Master_of = response.xpath('//*[@id="c3859"]/header/a').getall() korrigieren

        # Daten als csv speichern
        data = [{'Master_of': m, 'Studiengang': s, 'Link': l} for m, s, l in zip(Master_of, Studiengang, Link)]
        df = pd.DataFrame(data)
        df.to_csv('masterstudiengang_base_fhgr.csv')



# Vorgehen starten im Terminal:
# 1. cd "C:\Users\mguen\OneDrive\Desktop\Abfrage"
# 2. d:
# 3. scrapy crawl masterstudiengang_fhgr


# Check im Terminal:
# 1. cd C:\Users\mguen\OneDrive\Desktop\Abfrage
# 2. d:
# 3. scrapy shell
# 4. r = scrapy.Request(url="https://www.fhgr.ch/studium/masterangebot")        (Link ändern)
# 5. fetch(r)
# 6. response.body
# 7. response.xpath('//h4/text()').getall()     (hier in Klammer anpassen, je nach xpath vom Element)