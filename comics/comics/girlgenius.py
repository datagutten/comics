from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Girl Genius"
    language = "en"
    url = "http://www.girlgeniusonline.com/"
    start_date = "2002-11-04"
    rights = "Studio Foglio, LLC"


class Crawler(CrawlerBase):
    history_capable_date = "2002-11-04"
    schedule = "Mo,We,Fr"
    time_zone = "US/Pacific"

    def crawl(self, pub_date):
        url = "http://www.girlgeniusonline.com/ggmain/strips/ggmain%sb.jpg" % (
            pub_date.strftime("%Y%m%d"),
        )
        return CrawlerImage(url)
