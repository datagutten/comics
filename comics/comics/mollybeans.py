from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Molly Beans"
    language = "en"
    url = "http://www.mollybeans.com/"
    start_date = "2016-02-11"
    rights = "Dan Sacharow"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass
