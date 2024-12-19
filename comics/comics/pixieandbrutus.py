from comics.aggregator.crawler_webtoon import WebToonCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Pixie and Brutus"
    language = "en"
    url = "https://www.webtoons.com/en/canvas/pixie-and-brutus/list?title_no=452175"
    rights = "Pet Foolery"


class Crawler(WebToonCrawlerBase):
    # First date with a single release, catch up releases at 09
    history_capable_date = "2020-06-09"
