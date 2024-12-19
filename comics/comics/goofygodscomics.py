from comics.aggregator.crawler_webtoon import WebToonCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Goofy Gods Comics"
    language = "en"
    url = "https://www.webtoons.com/en/canvas/goofygodscomics/list?title_no=347186"
    rights = "GoofyGodsComics"


class Crawler(WebToonCrawlerBase):
    history_capable_date = "2019-10-20"
    has_rerun_releases = True
