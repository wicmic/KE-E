import scrapy
import pandas as pd

class Masterstudiengang_Details_FHNWSpider(scrapy.Spider):
    name = "masterstudiengang_details_fhnw"
    allowed_domains = ["www.fhnw.ch"]

    df = pd.read_csv('D:\Python\KE-E\Scrapy_KEE\Scrapy_KEE\masterstudiengang_base_fhnw.csv') # Link anpassen
    start_urls = df['Link'].tolist() # Daten aus df als Liste speichern

    def parse(self, response):
        Abschluss_official = response.xpath('//dt[text()="Abschluss"]/following-sibling::dd[1]/text()').get(default="keine Angaben vorhanden")
        Start = response.xpath('//dt[text()="Nächster Start"]/following-sibling::dd[1]/text()').get(default="keine Angaben vorhanden")
        Modus = response.xpath('//dt[text()="Studienmodus"]/following-sibling::dd[1]/text()').get(default="keine Angaben vorhanden")
        Dauer = response.xpath('//dt[text()="Dauer"]/following-sibling::dd[1]/text()').get(default="keine Angaben vorhanden")
        Semestergebühr = response.xpath('//dt[text()="Semestergebühr"]/following-sibling::dd[1]/text()').get(default="keine Angaben vorhanden")

        # Daten zu DataFrame hinzufügen
        self.df.loc[self.df['Link'] == response.url, 'Abschluss_official'] = Abschluss_official
        self.df.loc[self.df['Link'] == response.url, 'Start'] = Start
        self.df.loc[self.df['Link'] == response.url, 'Modus'] = Modus
        self.df.loc[self.df['Link'] == response.url, 'Dauer'] = Dauer
        self.df.loc[self.df['Link'] == response.url, 'Semestergebühr'] = Semestergebühr

    def closed(self, reason):
        # DataFrame mit den ergänzten Daten speichern
        self.df.to_csv('masterstudiengang_details_fhnw.csv', index=False)



# Vorgehen starten im Terminal:
# 1. cd "D:\Python\KE-E\Scrapy_KEE\Scrapy_KEE"
# 2. d:
# 3. scrapy crawl masterstudiengang_details_fhnw