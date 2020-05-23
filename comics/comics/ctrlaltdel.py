import requests

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Ctrl+Alt+Del"
    language = "en"
    url = "https://cad-comic.com/category/ctrl-alt-del/"
    start_date = "2002-10-23"
    rights = "Tim Buckley"


class Crawler(CrawlerBase):
    history_capable_date = "2002-10-23"
    schedule = "Mo,We,Fr"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        page_url = (
            "https://cad-comic.com/wp-admin/admin-ajax.php?"
            "action=custom_cat_search&post_cat=all&post_month=%s"
            % pub_date.strftime("%Y%m")
        )

        """req = urllib2.Request(page_url, None, self.headers)
        response = urllib2.urlopen(req)
        posts = json.load(response)"""

        response = requests.get(page_url)
        posts = response.json()

        if not posts["posts"]:
            return
        for post in posts["posts"]:
            try:
                date = self.string_to_date(post["date"], "%b %d, %Y")
            except ValueError:
                date = self.string_to_date(post["date"], "%B %d, %Y")

            if date == pub_date:
                return CrawlerImage(post["comic"], post["title"])
