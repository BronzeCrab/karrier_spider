import scrapy
from karrier.items import KarrierItem
from bs4 import BeautifulSoup
import urllib.parse


class KarSpider(scrapy.Spider):
    name = "kar"
    base_url = 'https://karriere.niedersachsen.de'
    start_urls = [
        base_url+'/index.asp?tree_id=195&typ='
        'prof&stype=suche&q=Suchbegriff&berufsgruppen=0&bvl=0&regionen'
        '=0&plz=PLZ&entfernung=20&nurfreie=1',
    ]

    def parse(self, response):
        # details_pages_a_1 = response.xpath(
        #     '//div[@class="listElement "]/text()')
        # lol = ''
        # for x in details_pages_a_1:
        #     lol += x.extract()[0]
        # import pdb;pdb.set_trace()
        # details_pages_a_2 = response.xpath(
        #     '//div[@class="listElement listeBg1"]/a[@target="_self"]')
        # details_pages_a_3 = response.xpath(
        #     '//div[@class="listElement listeBg2"]/a[@target="_self"]')
        # details_pages_a = details_pages_a_1+details_pages_a_2+details_pages_a_3

        soup = BeautifulSoup(response.body, "lxml")
        divs = soup.find_all("div", {"class": "listElement"})
        for div in divs:
            # print(urllib.parse.urljoin(self.base_url, details_page_link))
            item = KarrierItem()
            item['name'] = div.h3.text
            item['text'] = div.text
            item['url_to_pdf'] = urllib.parse.urljoin(
                self.base_url, div.find_all("a", "pdf")[0].attrs['href'])
            yield response.follow(
                urllib.parse.urljoin(self.base_url, div.a.attrs['href']),
                callback=self.parse_details,
                meta={'item': item})

    def parse_details(self, response):
        item = response.meta['item']
        yield item
