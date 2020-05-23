import unittest
from datetime import datetime

from comics.aggregator.crawler import NettserierCrawlerBase, today


class NettserierTestCrawler(NettserierCrawlerBase):
    short_name = None

    def __init__(self, short_name):
        super().__init__(None)
        self.short_name = short_name

    def crawl(self, pub_date):
        return self.crawl_helper(self.short_name, pub_date)

class NettserierTestCase(unittest.TestCase):
    def test_title_and_text(self):
        crawler = NettserierTestCrawler('stilleben')
        # date = crawler.string_to_date('2020-05-22', '%Y-%m-%d')
        date = datetime(2020, 5, 22).date()
        image = crawler.crawl(date)
        self.assertEqual('Stilleben 42', image.title)
        self.assertEqual(' Oppdateres hver onsdag og fredag!', image.text)
        self.assertEqual('https://nettserier.no/_ns/files/8d4bc59b7ac6f0512b7e88a0a69af7a8.jpg', image.url)

    def test_no_text(self):
        crawler = NettserierTestCrawler('wyyrd')
        # date = crawler.string_to_date('2020-05-22', '%Y-%m-%d')
        date = datetime(2016, 3, 14).date()
        image = crawler.crawl(date)
        self.assertEqual('183', image.title)
        self.assertEqual(None, image.text)
        self.assertEqual('https://nettserier.no/_ns/files/398b9cd9cfdf3cd8c363399137625f5c.png', image.url)

    def test_no_title_no_text(self):
        crawler = NettserierTestCrawler('hakkum')
        date = datetime(2020, 5, 18).date()
        image = crawler.crawl(date)
        self.assertEqual(None, image.title)
        self.assertEqual(None, image.text)
        self.assertEqual('https://nettserier.no/_ns/files/9c56cb218546d8c27c0eb7b4bf5238f0.png', image.url)

    def test_title_no_text(self):
        crawler = NettserierTestCrawler('prim')
        date = datetime(2008, 12, 30).date()
        image = crawler.crawl(date)
        self.assertEqual(None, image.title)
        self.assertEqual('Denne tror jeg har vært på trykk i Pondus. Siste Prim for denne gang. Produksjon av ferskvare er foreløpig i det blå.', image.text)
        self.assertEqual('https://nettserier.no/_ns/files/04660537a67b7cf807cd45272c121451.png', image.url)


if __name__ == '__main__':
    unittest.main()
