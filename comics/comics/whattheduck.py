from comics.aggregator.tumblr import TumblrCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "What the Duck"
    language = "en"
    url = "http://www.whattheduck.net/"
    start_date = "2006-07-01"
    rights = "Aaron Johnson"
    active = False


class Crawler(TumblrCrawlerBase):
    history_capable_date = "2006-07-20"
    time_zone = "US/Central"

    def crawl(self, pub_date):
        return self.crawl_helper(pub_date, "wtdcomics")
