from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Spiked Math"
    language = "en"
    url = "http://www.spikedmath.com/"
    start_date = "2009-08-24"
    rights = "Mike, CC BY-NC-SA 2.5"


class Crawler(CrawlerBase):
    history_capable_days = 20
    time_zone = "US/Mountain"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://feeds.feedburner.com/SpikedMath")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            result = []
            for url in page.src(
                'div.asset-body img[src*="/comics/"]', allow_multiple=True
            ):
                result.append(CrawlerImage(url))
            if result:
                result[0].title = entry.title
            return result
