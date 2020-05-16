from comics.aggregator.crawler import StartsidenCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Singelliv'
    language = 'no'
    url = 'https://www.startsiden.no/tegneserier/'
    rights = 'Charlotte Helgeland'


class Crawler(StartsidenCrawlerBase):
    history_capable_date = '2020-03-11'
    comic_name = 'Singelliv'

    def crawl(self, pub_date):
        return self.crawl_helper(pub_date)
