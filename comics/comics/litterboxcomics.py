from comics.aggregator.crawler_webtoon import WebToonCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Litterbox Comics"
    language = "en"
    url = "https://www.webtoons.com/en/canvas/litterbox-comics/list?title_no=196742"
    rights = "Chesca Hause"


class Crawler(WebToonCrawlerBase):
    history_capable_date = "2018-06-25"
    has_rerun_releases = True
    schedule = "Tu"
