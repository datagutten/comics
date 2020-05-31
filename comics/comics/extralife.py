from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "ExtraLife"
    language = "en"
    url = "http://www.myextralife.com/"
    start_date = "2001-06-17"
    rights = "Scott Johnson"
    active = False


class Crawler(CrawlerBase):
    history_capable_date = "2001-06-17"
    schedule = "Mo"
    time_zone = "US/Mountain"

    # Without User-Agent set, the server returns empty responses
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        year = int(pub_date.strftime("%Y"))

        if year > 2019:  # More recent year give 404
            return
        elif 2017 >= year >= 2011:
            url_year = pub_date.strftime("%Y") + "g"
        elif year == 2010:
            url_year = "2010b"
        elif year <= 2003:
            url_year = "01-03"
        else:
            url_year = pub_date.strftime("%Y")

        feed = self.parse_feed(
            "https://www.frogpants.com/%s?format=rss" % url_year
        )
        images = []
        # for entry in feed.for_date(pub_date):
        for entry in feed.all():
            url = entry.media_content[0]["url"]
            title = entry.title
            date = self.string_to_date(
                entry.published, "%a, %d %b %Y %H:%M:%S %z"
            )

            if url.find(pub_date.strftime("%Y-%m-%d")) > -1:
                images.append(CrawlerImage(url, title))
            elif date == pub_date:
                images.append(CrawlerImage(url, title))

        return images
