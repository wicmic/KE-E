import scrapy
import pandas as pd
import re
from urllib.parse import urljoin

class Masterstudiengang_FHGRSpider(scrapy.Spider):
    name = "masterstudiengang_fhgr"
    allowed_domains = ["www.fhgr.ch"]
    start_urls = ["https://www.fhgr.ch/studium/masterangebot"]

    def parse(self, response):
        # XPath-Abfrage für die Studiengänge
        Studiengang = response.xpath('//h4//text()').getall()

        # Entfernen von überflüssigen Zeilenumbrüchen und Leerzeichen
        reformatted_studiengaenge = [re.sub(r'\n\s+', ' ', course).strip() for course in Studiengang]

        # XPath-Abfrage für die Links
        relative_links = response.css('.StudyPath.StudyPath--GridItem a::attr(href)').getall()

        # Erstellen von vollständigen Links
        base_url = 'https://www.fhgr.ch'
        full_links = [urljoin(base_url, link) for link in relative_links]

        # Erstellen vom DataFrame und Speichern in einer CSV-Datei
        data = [{'Studiengang': s, 'Link': l} for s, l in zip(reformatted_studiengaenge, full_links)]
        df = pd.DataFrame(data)
        df.to_csv('masterstudiengang_base_fhgr.csv')


# Vorgehen Start im Terminal:
# 1. cd C:\Users\mguen\OneDrive\Desktop\abfragefhgr\abfragefhgr\abfragefhgr\spiders
# 2. C:
# 3. scrapy crawl masterstudiengang_fhgr

# Check im Terminal:
# 1. cd C:\Users\mguen\OneDrive\Desktop\abfragefhgr
# 2. d:
# 3. scrapy shell
# 4. r = scrapy.Request(url="https://www.fhgr.ch/studium/masterangebot")
# 5. fetch(r)
# 6. response.body
# 7. response.xpath('//h4//text()').getall()     (hier in Klammer anpassen, je nach xpath vom Element)