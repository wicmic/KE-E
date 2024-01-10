import scrapy
import pandas as pd

class Masterstudiengang_DetailsFHGRSpider(scrapy.Spider):
    name = "masterstudiengang_details_fhgr"
    allowed_domains = ["www.fhgr.ch"]

    df = pd.read_csv(r'masterstudiengang_base_fhgr.csv')  # Link anpassen
    start_urls = df['Link'].tolist()  # Daten aus df als Liste speichern

    def parse(self, response):
        Master_of = ' '.join(response.xpath('//div//li[contains(.,"Abschluss")]/text()').get(default="keine Angaben vorhanden").strip().split()[:3])
        Abschluss_official = response.xpath('//div//li[contains(.,"Abschluss")]/text()').get(default="keine Angaben vorhanden").strip()
        Start = response.xpath('//div//li[contains(.,"Studienbeginn")]/text()').get(default="keine Angaben vorhanden").strip()
        Modus = response.xpath('//div//li[contains(.,"Studienmodell")]/text()').get(default="keine Angaben vorhanden").strip()
        Dauer = response.xpath('//div//li[contains(.,"Studiendauer")]/text()').get(default="keine Angaben vorhanden").strip()
        Semestergebühr = ' '.join(map(str.strip, response.xpath('//p[contains(., "Die Studiengebühr beträgt")]/text() | //p[contains(., "Die Studiengebühr beträgt")]/strong/text() | //p[contains(.,"Die beträgt")]/strong/text() | //p[contains(.,"Die beträgt")]/text()').getall())).strip()
        if not Semestergebühr:
            Semestergebühr = "keine Angaben vorhanden"

        # Daten zu DataFrame hinzufügen
        self.df.loc[self.df['Link'] == response.url, 'Master_of'] = Master_of
        self.df.loc[self.df['Link'] == response.url, 'Abschluss_official'] = Abschluss_official
        self.df.loc[self.df['Link'] == response.url, 'Start'] = Start
        self.df.loc[self.df['Link'] == response.url, 'Modus'] = Modus
        self.df.loc[self.df['Link'] == response.url, 'Dauer'] = Dauer
        self.df.loc[self.df['Link'] == response.url, 'Semestergebühr'] = Semestergebühr

    def closed(self, reason):
        # Reihenfolge der Spalten ändern
        self.df = self.df[['Unnamed: 0', 'Master_of', 'Studiengang', 'Link', 'Abschluss_official', 'Start', 'Modus', 'Dauer', 'Semestergebühr']]
        # DataFrame mit den ergänzten Daten speichern
        self.df.to_csv('masterstudiengang_details_fhgr.csv', index=False)


# Vorgehen starten im Terminal:
# 1. cd C:\Users\mguen\OneDrive\Desktop\abfragefhgr\abfragefhgr\abfragefhgr\spiders
# 2. C:
# 3. scrapy crawl masterstudiengang_details_fhgr
