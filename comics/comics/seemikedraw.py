from comics.aggregator.tumblr import TumblrCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "seemikedraw"
    language = "en"
    url = "http://mikejacobsen.tumblr.com/"
    start_date = "2007-07-31"
    end_date = "2017-04-06"
    rights = "Mike Jacobsen"
    active = False


class Crawler(TumblrCrawlerBase):
    history_capable_date = "2013-01-30"
    time_zone = "Australia/Sydney"

    def crawl(self, pub_date):
        return self.crawl_helper("mikejacobsen", pub_date)
