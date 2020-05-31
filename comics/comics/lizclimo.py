from comics.aggregator.tumblr import TumblrCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Hi, I'm Liz"
    language = "en"
    url = "http://lizclimo.tumblr.com/"
    start_date = "2011-12-15"
    rights = "Liz Climo"


class Crawler(TumblrCrawlerBase):
    history_capable_date = "2011-12-15"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        return self.crawl_helper("lizclimo", pub_date)
