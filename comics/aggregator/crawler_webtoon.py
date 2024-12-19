import math
from datetime import datetime

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.aggregator.lxmlparser import LxmlParser


def get_page_count(front_page: LxmlParser) -> int:
    pages = front_page.root.xpath('.//div[@class="paginate"]/a/span')
    page_next = front_page.root.xpath('.//div[@class="paginate"]/a[@class="pg_next"]')
    if page_next:
        episodes = front_page.root.xpath('.//li[@class="_episodeItem"]')
        episodes_per_page = len(episodes)
        first_episode_num = episodes[0].xpath('./a/span[@class="tx"]/.')[0].text[1:]
        return math.ceil(int(first_episode_num) / episodes_per_page)

    return len(pages)


class WebToonCrawlerBase(CrawlerBase):
    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36",
    }

    def get_episode(self, page_url):
        release_images = []
        episode_page = self.parse_page(page_url)
        images = episode_page.root.xpath('.//div[@id="_imageList"]/img')
        title = episode_page.root.xpath('.//h1[@class="subj_episode"]')

        for image in images:
            url = image.get("data-url")
            release_images.append(
                CrawlerImage(url, title, request_headers={"Referer": page_url})
            )
            if not self.has_rerun_releases:
                title = None

        return release_images

    def crawl(self, pub_date: datetime.date) -> CrawlerResult:
        if self.comic.end_date and pub_date > self.comic.end_date:
            return
        page_count: int = 0
        front_page = self.parse_page(self.comic.url)
        if not page_count:
            page_count = get_page_count(front_page)
        for page_num in range(1, page_count + 1):
            page = self.parse_page("%s&page=%d" % (self.comic.url, page_num))
            episodes = page.root.xpath('.//li[@class="_episodeItem"]')
            for episode in episodes:
                date_string = episode.xpath('.//span[@class="date"]')[0].text.strip()
                date = datetime.strptime(date_string, "%b %d, %Y").date()
                # If we have passed the requested date without returning,
                # there is no release for the requested day
                if date < pub_date:
                    return

                if date == pub_date:
                    link = episode.xpath("./a")[0].get("href")
                    return self.get_episode(link)
