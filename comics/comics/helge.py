from comics.aggregator.crawler import StartsidenCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Helge"
    language = "no"
    url = "https://www.startsiden.no/tegneserier/"
    rights = "Lars Mortimer"


class Crawler(StartsidenCrawlerBase):
    history_capable_date = "2019-03-08"
    comic_name = "Helge"

    def crawl(self, pub_date):
        return self.crawl_helper(pub_date)
