from comics.aggregator.tumblr import TumblrCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Garfield minus Garfield"
    language = "en"
    url = "http://garfieldminusgarfield.tumblr.com/"
    rights = "Travors"


class Crawler(TumblrCrawlerBase):
    history_capable_date = "2008-02-13"
    schedule = None
    time_zone = "Europe/London"

    def crawl(self, pub_date):
        return self.crawl_helper("garfieldminusgarfield", pub_date)
