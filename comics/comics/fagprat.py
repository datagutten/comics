# encoding: utf-8

from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Fagprat (db.no)"
    language = "no"
    url = "http://www.dagbladet.no/tegneserie/fagprat"
    rights = "Flu Hartberg"
    active = False


class Crawler(DagbladetCrawlerBase):
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        return self.crawl_helper("fagprat", pub_date)
