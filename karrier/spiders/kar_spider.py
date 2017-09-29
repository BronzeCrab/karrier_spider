# -*- coding: utf-8 -*-

import scrapy
from karrier.items import KarrierItem
from bs4 import BeautifulSoup
import urlparse
import re
import sys


class KarSpider(scrapy.Spider):
    name = "kar"
    base_url = 'https://karriere.niedersachsen.de'
    start_urls = [
        base_url+'/index.asp?tree_id=195&typ='
        'prof&stype=suche&q=Suchbegriff&berufsgruppen=0&bvl=0&regionen'
        '=0&plz=PLZ&entfernung=20&nurfreie=1',
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        divs = soup.find_all("div", {"class": "listElement"})
        for div in divs:
            item = KarrierItem()
            item['name'] = div.h3.text
            # einstellungsdatum
            if not div.span.text:
                print ("Warning, no Einstellungsdatum match")
                sys.exit()
            elif ':' in div.span.text:
                item['einstellungsdatum'] = div.span.text.split(':')[1].strip()
            else:
                item['einstellungsdatum'] = div.span.text

            div_text = div.text
            div_text = div_text.replace('\r', ' ').replace(
                '\n', ' ').replace('\t', ' ')

            # address
            match = re.search(
                r"Einstellungsdatum:[ \d.]*(.*)Stellenumfang", div_text)
            if match:
                item['address'] = match.group(1)
            else:
                # try another variant
                match = re.search(
                    r"Zeitpunkt(.*)Stellenumfang", div_text)
                if match:
                    item['address'] = match.group(1)
                else:
                    print ("Warning, no adrress match")
                    sys.exit()
            # stellenumfang
            match = re.search(r"Stellenumfang:([ \d.]*)", div_text)
            if match:
                item['stellenumfang'] = match.group(1).strip()
            else:
                print ("Warning, no stellenumfang match")
                sys.exit()
            # platze
            match = re.search(u"Pl\xe4tze:([ \d.]*)", div_text)
            if match:
                item['platze'] = match.group(1).strip()
            else:
                print ("Warning, no Plätze match")
                sys.exit()
            # befristung
            match = re.search(
                r"Befristung:(.*)Besoldungs", div_text)
            if match:
                item['befristung'] = match.group(1).strip()
            else:
                print ("Warning, no befristung match")
                sys.exit()
            # besoldungs
            match = re.search(
                r"Besoldungs-/Entgeltgruppe:(.*)Stellennummer", div_text)
            if match:
                item['besoldungs'] = match.group(1).strip()
            else:
                print ("Warning, no besoldungs match")
                sys.exit()
            # stellennummer
            match = re.search(
                r"Stellennummer:([ \d.]*)", div_text)
            if match:
                item['stellennummer'] = match.group(1).strip()
            else:
                print ("Warning, no stellennummer match")
                sys.exit()

            item['text'] = div_text.strip()
            item['url_to_pdf'] = urlparse.urljoin(
                self.base_url, div.find_all("a", "pdf")[0].attrs['href'])
            yield response.follow(
                urlparse.urljoin(self.base_url, div.a.attrs['href']),
                callback=self.parse_details,
                meta={'item': item})

    def parse_details(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body, "lxml")
        div = soup.find_all("div", {"class": "ausbildungsplaetze"})[0]
        item['place'] = div.h3.text
        table = soup.find_all("table", {"class": "listeBg3"})[0]
        item['additional_text'] = table.text
        div = soup.find_all("div", {"class": "Stelle"})[0]
        item['detailed_data'] = div.text
        yield item
