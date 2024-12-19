from comics.aggregator.crawler_webtoon import WebToonCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Emmy the Robot"
    language = "en"
    url = "https://www.webtoons.com/en/canvas/emmy-the-robot/list?title_no=402201"
    rights = "Domcell"


class Crawler(WebToonCrawlerBase):
    history_capable_date = "2020-04-05"
    has_rerun_releases = True  # Releases include a common header image
