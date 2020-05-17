from urllib.error import HTTPError

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


def get_history_capable_date():
    comics = []
    for slug in get_comic_module_names():
        module = get_comic_module(slug)
        if module.Crawler.history_capable_date is not None:
            comics.append(slug)

    return comics


def get_history_capable_days():
    comics = []
    for slug in get_comic_module_names():
        module = get_comic_module(slug)
        # crawler = module.Crawler(comic)
        if module.Crawler.history_capable_days is not None:
            comics.append(slug)


@ddt
class CrawlersTestCase(TestCase):
    @idata(get_comic_module_names())
    def test_crawl(self, slug):
        options = {'comic_slugs': [slug]}
        print('Crawl %s' % slug)
        data_loader = ComicDataLoader(options)
        data_loader.start()

        """aggregator = Aggregator(options=options)
        aggregator.start()"""

        comic = Comic.objects.get(slug=slug)
        module = get_comic_module(slug)
        crawler = module.Crawler(comic)
        pub_date = crawler.history_capable


        try:
            images = crawler.crawl(pub_date)
        except HTTPError as e:
            if e.code == 404:
                self.skipTest(e.msg)
                return
            else:
                raise e

        if images is None:
            self.skipTest('No release for %s %s' % (slug, pub_date))
        else:
            if not hasattr(images, '__iter__'):
                images = [images]
            for image in images:
                self.assertIsInstance(image, CrawlerImage)
                self.assertIsNotNone(image.url, 'Crawler returned image without URL')

    @idata(get_history_capable_date())
    def test_history_capability(self, slug):
        options = {'comic_slugs': [slug]}

        data_loader = ComicDataLoader(options)
        data_loader.start()

        """comic = Comic.objects.get(slug=slug)
        module = get_comic_module(slug)
        crawler = module.Crawler(comic)"""
        crawler = get_crawler(slug)

        if crawler.history_capable_date is None: # and crawler.history_capable_days is None:
            return

        history_date = crawler.history_capable
        try:
            images = crawler.crawl(history_date)
        except HTTPError as e:
            self.fail(e.msg)

        self.assertIsNotNone(images, 'No images found for date %s' % history_date)

        if not hasattr(images, '__iter__'):
            images = [images]
        for image in images:
            self.assertIsInstance(image, CrawlerImage)
            self.assertIsNotNone(image.url, 'Crawler returned image without URL for date %s' % history_date)
