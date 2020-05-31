from comics.aggregator.tumblr import TumblrCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Cardboard Crack"
    language = "en"
    url = "http://cardboard-crack.com/"
    start_date = "2013-03-01"
    rights = "Magic Addict"
    active = False


class Crawler(TumblrCrawlerBase):
    history_capable_date = "2013-03-25"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "US/Pacific"

    def crawl(self, pub_date):
        return self.crawl_helper("cardboard-crack", pub_date)
