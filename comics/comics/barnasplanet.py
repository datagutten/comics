from comics.aggregator.crawler import StartsidenCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Barnas Planet'
    language = 'no'
    url = 'https://www.startsiden.no/tegneserier/'
    rights = 'Lars Rudebjer'


class Crawler(StartsidenCrawlerBase):
    history_capable_date = '2019-07-04'
    comic_name = 'Barnas Planet'

    def crawl(self, pub_date):
        return self.crawl_helper(pub_date)
