from comics.aggregator.tumblr import TumblrCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Sarah's Scribbles"
    language = "en"
    url = "http://www.sarahcandersen.com/"
    start_date = "2011-01-01"
    rights = "Sarah Andersen"


class Crawler(TumblrCrawlerBase):
    history_capable_days = 60
    schedule = "We,Sa"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        return self.crawl_helper("sarahseeandersen", pub_date)
