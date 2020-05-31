from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Piled Higher and Deeper"
    language = "en"
    url = "http://www.phdcomics.com/"
    start_date = "1997-10-27"
    end_date = "2018-12-24"
    rights = "Jorge Cham"
    active = False


class Crawler(CrawlerBase):
    history_capable_date = ComicData.start_date
    schedule = None
    time_zone = "US/Pacific"

    def crawl(self, pub_date):
        page = self.parse_page('http://phdcomics.com/comics/archive_list.php')
        release = page.root.xpath('//a/b[.="%s"]/../@href' % pub_date.strftime('%-m/%-d/%Y'))
        if not release:
            return

        release_page = self.parse_page(release[0])
        title = release_page.content('meta[name="twitter:title"]')
        url = release_page.href('link[rel="image_src"]')

        return CrawlerImage(url, title)
