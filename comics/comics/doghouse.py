from django.utils.dateformat import DateFormat

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The Doghouse Diaries"
    language = "en"
    url = "http://www.thedoghousediaries.com/"
    start_date = "2009-01-08"
    rights = "Will, Ray, & Raf"
    active = False


class Crawler(CrawlerBase):
    history_capable_date = "2009-01-08"
    schedule = "Mo,We,Fr"
    time_zone = "US/Pacific"

    def crawl(self, pub_date):
        page = self.parse_page("http://thedoghousediaries.com/archive")

        tables = page.root.xpath(
            '//div[@id="%s"]/following-sibling::table'
            % pub_date.strftime("%Y")
        )
        if not tables:  # No releases that year
            return

        table = tables[0]
        date = DateFormat(pub_date).format("F jS")
        releases = table.xpath('tr/td[.="%s"]/../td/a' % date)
        if not releases:  # No release that date
            return

        images = []
        for release in releases:
            title = release.text
            page = self.parse_page(release.get("href"))
            url = page.src("div#imgdiv img")
            images.append(CrawlerImage(url, title))

        return images
