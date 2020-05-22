from comics.aggregator.crawler import ComicsKingdomCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Sherman's Lagoon"
    language = "en"
    url = "http://shermanslagoon.com/"
    start_date = "1991-05-13"
    rights = "Jim Toomey"


class Crawler(ComicsKingdomCrawlerBase):
    history_capable_days = 6

    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        return self.crawl_helper("sherman-s-lagoon", pub_date)
