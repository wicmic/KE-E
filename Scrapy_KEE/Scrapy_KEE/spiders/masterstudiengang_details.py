import scrapy
import pandas as pd
import csv

class Masterstudiengang_DetailsSpider(scrapy.Spider):
    name = "masterstudiengang_details"
    allowed_domains = ["www.fhnw.ch"]
    start_urls = ["https://www.fhnw.ch/de/studium/psychologie/master-angewandte-psychologie"]

    def parse(self, response):
        Abschluss_official = response.xpath('//dt[text()="Abschluss"]/following-sibling::dd[1]/text()').get(default="keine Angaben vorhanden")
        Start = response.xpath('//dt[text()="Nächster Start"]/following-sibling::dd[1]/text()').get(default="keine Angaben vorhanden")
        Modus = response.xpath('//dt[text()="Studienmodus"]/following-sibling::dd[1]/text()').get(default="keine Angaben vorhanden")
        Dauer = response.xpath('//dt[text()="Dauer"]/following-sibling::dd[1]/text()').get(default="keine Angaben vorhanden")
        Semestergebühr = response.xpath('//dt[text()="Semestergebühr"]/following-sibling::dd[1]/text()').get(default="keine Angaben vorhanden")


        # Daten als csv speichern
        data = {'Abschluss_official': [Abschluss_official], 'Start': [Start], 'Modus': [Modus], 'Dauer': [Dauer],
                'Semestergebühr': [Semestergebühr]}
        df = pd.DataFrame(data)
        df.to_csv('masterstudiengang_details.csv')



# Vorgehen starten im Terminal:
# 1. cd "D:\Python\KE-E\Scrapy_KEE\Scrapy_KEE"
# 2. d:
# 3. scrapy crawl masterstudiengang_details