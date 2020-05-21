# encoding: utf-8

from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Rutetid"
    language = "no"
    url = "http://www.dagbladet.no/tegneserie/rutetid/"
    rights = "Frode Øverli"
    active = False


class Crawler(DagbladetCrawlerBase):
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        return self.crawl_helper("rutetid", pub_date)
