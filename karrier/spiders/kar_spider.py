import scrapy
from karrier.items import KarrierItem
from bs4 import BeautifulSoup
import urlparse


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
            item['text'] = div.text.strip()
            item['einstellung'] = div.span.text
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
        yield item
