import scrapy
import pandas as pd
import csv

class Masterstudiengang_DetailsSpider(scrapy.Spider):
    name = "masterstudiengang_details"
    allowed_domains = ["www.fhnw.ch"]

    df = pd.read_csv('D:\Python\KE-E\Scrapy_KEE\Scrapy_KEE\masterstudiengang_base.csv') # Link anpassen
    start_urls = df['Link'].tolist() # Daten aus df als Liste speichern

    #start_urls = ['https://www.fhnw.ch/de/studium/psychologie/master-angewandte-psychologie',
                  #'https://www.fhnw.ch/de/studium/architektur-bau-geomatik/master-studiengang-architektur',
                  #'https: // www.fhnw.ch / de / studium / architektur - bau - geomatik / master - of - science - fhnw - in -engineering - mse', # keine Einträge vorhanden
                  #'https://www.fhnw.ch/de/studium/gestaltung-kunst/master-of-arts/master-of-arts-fhnw-in-design-digital-communication-environments'] # 4 Beispiele

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
        df.to_csv('masterstudiengang_details.csv', mode='a', header=False)



# Vorgehen starten im Terminal:
# 1. cd "D:\Python\KE-E\Scrapy_KEE\Scrapy_KEE"
# 2. d:
# 3. scrapy crawl masterstudiengang_details