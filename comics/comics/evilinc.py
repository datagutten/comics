from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Evil Inc."
    language = "en"
    url = "http://evil-inc.com/"
    start_date = "2005-05-30"
    rights = "Brad J. Guigar - Colorist: Ed Ryzowski"


class Crawler(CrawlerBase):
    history_capable_date = "2017-10-05"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed('https://evil-inc.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/wp-content/uploads/"]')
            title = entry.title
            return CrawlerImage(url, title)
