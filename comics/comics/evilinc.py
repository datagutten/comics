from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.aggregator.exceptions import CrawlerError
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Evil Inc."
    language = "en"
    url = "http://evil-inc.com/"
    start_date = "2005-05-30"
    rights = "Brad J. Guigar - Colorist: Ed Ryzowski"


class Crawler(CrawlerBase):
    history_capable_date = "2018-01-16"
    time_zone = "US/Eastern"

    def get_page(self, page_num=1):
        url = "https://evil-inc.com/comic"
        if page_num > 1:
            url += "/page/%d/" % page_num

        page = self.parse_page(url)

        dates = page.root.xpath('//p[@class="comic-post-date"]')

        if not dates:
            raise CrawlerError(
                self.comic, "No dates found on page %d" % page_num
            )

        first_date = self.string_to_date(dates[-1].text, "%b %d, %Y")
        return page, first_date

    def crawl(self, pub_date):
        page, first_date = self.get_page()
        page_num = 2
        while pub_date < first_date:
            page, first_date = self.get_page(page_num)
            page_num += 1
            if not page:
                return

        if pub_date == self.current_date:
            date = "Today"
        else:
            date = pub_date.strftime("%b %d, %Y")

        release = page.root.xpath(
            '//p[@class="comic-post-date" and .="%s"]' % date
        )

        if not release:
            return
        link = release[0].xpath('ancestor::div[@class="comic-item"]/../@href')
        release_page = self.parse_page(link[0])

        url = release_page.src("div#unspliced-comic img")
        title = release_page.text("h1.entry-title")

        return CrawlerImage(url, title)
