import scrapy
import pandas as pd

class Masterstudiengang_DetailsSpider(scrapy.Spider):
    name = "masterstudiengang_details_fhgr"
    allowed_domains = ["www.fhgr.ch"]

    df = pd.read_csv(r'masterstudiengang_base_fhgr.csv') # Link anpassen
    start_urls = df['Link'].tolist() # Daten aus df als Liste speichern

    def parse(self, response):
        Abschluss_official = response.xpath('//h4[contains(text(), "Abschluss")]/following-sibling::div[1]/text()').get(default="keine Angaben vorhanden")
        Start = response.xpath('//h4[contains(text(), "Studienbeginn")]/following-sibling::div[1]/text()').get(default="keine Angaben vorhanden")
        Modell = response.xpath('//h4[contains(text(), "Studienmodell")]/following-sibling::div[1]/text()').get(default="keine Angaben vorhanden")
        Dauer = response.xpath('//h4[contains(text(), "Studiendauer")]/following-sibling::div[1]/text()').get(default="keine Angaben vorhanden")
        Semestergebühr = response.xpath('//h4[contains(text(), "Semestergebühr")]/following-sibling::div[1]/text()').get(default="keine Angaben vorhanden")

        # Daten zu DataFrame hinzufügen
        self.df.loc[self.df['Link'] == response.url, 'Abschluss_official'] = Abschluss_official
        self.df.loc[self.df['Link'] == response.url, 'Start'] = Start
        self.df.loc[self.df['Link'] == response.url, 'Modell'] = Modell
        self.df.loc[self.df['Link'] == response.url, 'Dauer'] = Dauer
        self.df.loc[self.df['Link'] == response.url, 'Semestergebühr'] = Semestergebühr

    def closed(self, reason):
        # DataFrame mit den ergänzten Daten speichern
        self.df.to_csv('masterstudiengang_details_fhgr.csv', index=False)

# Vorgehen starten im Terminal:
# 1. cd C:\Users\mguen\OneDrive\Desktop\KE-E\Scrapy_KEE\Scrapy_KEE
# 2. d:
# 3. scrapy crawl masterstudiengang_details_fhgr