import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The Joy of Tech"
    language = "en"
    url = "http://www.geekculture.com/joyoftech/"
    start_date = "2000-08-14"
    rights = "Geek Culture"


class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = "Mo,We,Fr"
    time_zone = "America/New_York"

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.joyoftech.com/joyoftech/jotblog/atom.xml")
        for entry in feed.for_date(pub_date):
            title = entry.title

            matches = re.search(r"joyarchives/(\d+)\.html", str(entry.link))
            if matches is None:
                continue
            num = matches.group(1)

            page = self.parse_page(entry.link)
            url = page.src('img[src*="/joyimages/%s"]' % num)
            if not url:
                continue
            return CrawlerImage(url, title)
