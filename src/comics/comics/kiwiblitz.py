from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Kiwi Blitz"
    language = "en"
    url = "http://www.kiwiblitz.com/"
    start_date = "2009-04-18"
    rights = "Mary Cagle"


class Crawler(ComicControlCrawlerBase):
    history_capable_days = 180
    schedule = "Th"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        return self.crawl_helper(ComicData.url, pub_date)
