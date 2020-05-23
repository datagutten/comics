import os
from datetime import datetime, timedelta

import requests
from ddt import ddt, idata
from django.test import TestCase

from comics.aggregator.crawler import CrawlerImage
from comics.comics import get_comic_module, get_comic_module_names
from comics.core.comic_data import ComicDataLoader
from comics.core.models import Comic


def get_crawler(slug):
    comic = Comic.objects.get(slug=slug)
    module = get_comic_module(slug)
    return module.Crawler(comic)


def get_comics():
    comics = get_comic_module_names()
    if 'COMIC' in os.environ and os.environ['COMIC'] in comics:
        return [os.environ['COMIC']]
    else:
        return comics


def get_history_capable_date():
    comics = []
    for slug in get_comics():
        module = get_comic_module(slug)
        if module.Crawler.history_capable_date is not None:
            comics.append(slug)

    return comics


def get_history_capable_days():
    comics = []
    for slug in get_comics():
        module = get_comic_module(slug)
        if module.Crawler.history_capable_days is not None:
            comics.append(slug)
    return comics


def get_last_date(slug):
    # TODO: Check schedule to get day
    module = get_comic_module(slug)
    schedule = module.Crawler.schedule
    schedule = schedule.split(',')
    return datetime.today().date()


@ddt
class CrawlersTestCase(TestCase):
    def crawl(self, crawler, pub_date):
        try:
            return crawler.crawl(pub_date)
        except requests.exceptions.HTTPError as e:
            if e.errno == 404:
                self.skipTest(e)
                return
            else:
                raise e

    @idata(get_comics())
    def test_crawl(self, slug):
        options = {'comic_slugs': [slug]}
        # print('Crawl %s' % slug)
        data_loader = ComicDataLoader(options)
        data_loader.start()

        """aggregator = Aggregator(options=options)
        aggregator.start()"""

        comic = Comic.objects.get(slug=slug)
        module = get_comic_module(slug)
        crawler = module.Crawler(comic)
        pub_date = datetime.today().date()

        images = self.crawl(crawler, pub_date)

        if images is None:
            self.skipTest('No release for %s %s' % (slug, pub_date))
        else:
            if not hasattr(images, '__iter__'):
                images = [images]
            for image in images:
                self.assertIsInstance(image, CrawlerImage)
                self.assertIsNotNone(image.url, 'Crawler returned image without URL for date %s' % pub_date)

    @idata(get_history_capable_date())
    def test_history_capability(self, slug):
        options = {'comic_slugs': [slug]}

        data_loader = ComicDataLoader(options)
        data_loader.start()

        """comic = Comic.objects.get(slug=slug)
        module = get_comic_module(slug)
        crawler = module.Crawler(comic)"""
        crawler = get_crawler(slug)

        history_date = crawler.history_capable
        try:
            images = crawler.crawl(history_date)
        except requests.exceptions.HTTPError as e:
            self.fail(e)

        self.assertIsNotNone(images, 'No images found for date %s' % history_date)

        if not hasattr(images, '__iter__'):
            images = [images]
        for image in images:
            self.assertIsInstance(image, CrawlerImage)
            self.assertIsNotNone(image.url, 'Crawler returned image without URL for date %s' % history_date)

    @idata(get_history_capable_days())
    def test_history_capability_days(self, slug):
        options = {'comic_slugs': [slug]}

        data_loader = ComicDataLoader(options)
        data_loader.start()

        crawler = get_crawler(slug)

        date_from = datetime.today() - timedelta(crawler.history_capable_days+10)
        date_to = datetime.today() - timedelta(crawler.history_capable_days-10)
        date = date_from
        images = None

        while date <= date_to:
            date = date + timedelta(1)
            images = self.crawl(crawler, date.date())
            if images is not None:
                break

        self.assertIsNotNone(images, 'No images found between %s and %s' % (date_from, date_to))

        if not hasattr(images, '__iter__'):
            images = [images]
        for image in images:
            self.assertIsInstance(image, CrawlerImage)
            self.assertIsNotNone(image.url, 'Crawler returned image without URL for date %s' % date)
