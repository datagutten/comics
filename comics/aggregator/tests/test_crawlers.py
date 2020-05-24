import os
import unittest
from datetime import datetime, timedelta

import requests
from ddt import ddt, idata

from comics.aggregator.crawler import CrawlerImage, today
from comics.comics import get_comic_module, get_comic_module_names


def get_crawler(slug):
    module = get_comic_module(slug)
    return module.Crawler(None)


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
    return []
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
class CrawlersTestCase(unittest.TestCase):
    def crawl(self, crawler, pub_date, allow_404=False):
        try:
            return crawler.crawl(pub_date)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404 and allow_404:
                self.skipTest(e)
                return
            else:
                raise e

    @idata(get_comics())
    def test_crawl(self, slug):
        options = {'comic_slugs': [slug]}
        # print('Crawl %s' % slug)
        crawler = get_crawler(slug)
        pub_date = datetime.today().date()

        images = self.crawl(crawler, pub_date, True)

        if images is None:
            self.skipTest('No release for %s %s' % (slug, pub_date))
        else:
            if not hasattr(images, '__iter__'):
                images = [images]
            for image in images:
                self.assertIsInstance(image, CrawlerImage)
                self.assertIsNotNone(image.url, 'Crawler returned image without URL for date %s' % pub_date)

    @idata(get_history_capable_date())
    def test_history_capable_date(self, slug):
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
        crawler = get_crawler(slug)

        date_from = today() - timedelta(crawler.history_capable_days+10)
        date_to = today() - timedelta(crawler.history_capable_days-10)
        if date_to>today():
            date_to = today()
        date = date_from
        images = None

        while date <= date_to:
            date = date + timedelta(1)
            images = self.crawl(crawler, date)
            if images is not None:
                if hasattr(images, '__iter__'):
                    images = images[0]
                    break
                if isinstance(images, CrawlerImage) and images.url:
                    break

        self.assertIsNotNone(images, 'No images found between %s and %s' % (date_from, date_to))

        if not hasattr(images, '__iter__'):
            images = [images]
        for image in images:
            self.assertIsInstance(image, CrawlerImage)
            self.assertIsNotNone(image.url, 'Crawler returned image without URL for date %s' % date)


if __name__ == "__main__":
    unittest.main()
