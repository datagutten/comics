# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.comics.pondus import ComicData as PondusData


class ComicData(PondusData):
    name = 'Pondus (bt.no)'
    url = 'http://www.bt.no/bergenpuls/tegneserier/tegneserier_pondus/'


class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        url = 'http://www.bt.no/external/cartoon/pondus/%s.gif' % (
            pub_date.strftime('%d%m%y'),)
        return CrawlerImage(url)
