from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Teh Gladiators"
    language = "en"
    url = "http://www.tehgladiators.com/book_cat/teh-gladiator"
    start_date = "2008-03-18"
    rights = "Uros Jojic & Borislav Grabovic"
    active = False


class Crawler(CrawlerBase):
    time_zone = "Europe/Belgrade"

    def crawl(self, pub_date):
        pass
