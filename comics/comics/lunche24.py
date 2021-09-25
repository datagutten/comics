# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Lunch (e24.no)"
    language = "no"
    url = "http://www.e24.no/lunch/"
    start_date = "2009-10-21"
    rights = "Børge Lund"


class Crawler(CrawlerBase):
    history_capable_date = "2021-07-01"
    schedule = "Mo,Tu,We,Th,Fr,Sa"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        url = "https://api.e24.no/content/v1/comics/%s" % (
            pub_date.strftime("%Y-%m-%d")
        )
        return CrawlerImage(url)
