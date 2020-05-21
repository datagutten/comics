# encoding: utf-8

from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Lille Berlin"
    language = "no"
    url = "http://www.dagbladet.no/tegneserie/lille-berlin/"
    rights = "Ellen Ekman"
    active = False


class Crawler(DagbladetCrawlerBase):
    history_capable_days = 14
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        return self.crawl_helper("lille-berlin", pub_date)
