from comics.aggregator.crawler_webtoon import WebToonCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Safely Endangered"
    language = "en"
    url = "https://www.webtoons.com/en/comedy/safely-endangered/list?title_no=352"
    rights = "Chris McCoy"


class Crawler(WebToonCrawlerBase):
    schedule = "Mo,We"
    history_capable_date = "2014-12-01"
    has_rerun_releases = True
