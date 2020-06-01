from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


def make_ordinal(n):
    """
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    https://stackoverflow.com/a/50992575/2630074
    """
    n = int(n)
    suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    return str(n) + suffix


class ComicData(ComicDataBase):
    name = "Dinosaur Comics"
    language = "en"
    url = "http://www.qwantz.com/"
    start_date = "2003-02-01"
    rights = "Ryan North"


class Crawler(CrawlerBase):
    history_capable_date = "2003-02-01"
    schedule = "Mo,Tu,We,Th"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        page = self.parse_page("http://www.qwantz.com/archive.php")
        # Format the date in the form "January 31st, 2020"
        date = "%s %s, %s" % (
            pub_date.strftime("%B"),
            make_ordinal(pub_date.strftime("%d")),
            pub_date.strftime("%Y"),
        )
        link = page.root.xpath('//a[.="%s"]' % date)

        if not link:
            return
        title = link[0].tail
        page_url = link[0].get("href")
        page = self.parse_page(page_url)
        url = page.src('img[src*="comics"]')
        text = page.title('img[src*="comics"]')

        return CrawlerImage(url, title, text)
