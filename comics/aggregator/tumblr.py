import re

import requests

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.aggregator.exceptions import CrawlerError, CrawlerHTTPError


class TumblrCrawlerBase(CrawlerBase):
    site = None  # Tumblr blog identifier
    api_token = None  # Tumblr API key
    posts = {}  # Post page cache
    headers = {'User-Agent': 'curl/7.64.0'}

    def get_api_token(self):
        try:
            page = self.parse_page("https://%s.tumblr.com/archive/" % self.site)
            token = page.root.xpath("//script[contains(.,'API_TOKEN')]")
            matches = re.search(r'"API_TOKEN":"(.+?)"', token[0].text)
            self.api_token = matches.group(1)
        except Exception as e:
            raise CrawlerError(self.site, "Unable to get API token: %s" % e)

    def get_posts(self, page=1):
        if not self.api_token:
            self.get_api_token()
        if page in self.posts:
            return self.posts[page]

        headers = {"authorization": "Bearer %s" % self.api_token}
        url = "https://api.tumblr.com/v2/blog/%s/posts/photo" % self.site
        if page > 1:
            url += "?offset=%d&page_number=%d" % ((page - 1) * 20, page)
        response = requests.get(url, headers=headers)
        if not response.status_code == 200:
            raise CrawlerHTTPError(self.site, response.status_code)
        posts = response.json()

        self.posts[page] = posts["response"]["posts"]  # Cache posts
        return posts["response"]["posts"]

    def crawl_posts(self, pub_date, page=1):
        posts = self.get_posts(page)
        date = None
        title = None
        text = None

        for post in posts:
            date = self.string_to_date(post["date"], "%Y-%m-%d %H:%M:%S %Z")
            if not date == pub_date:
                continue

            if not post["content"]:
                continue
            if "summmary" in post:
                title = post["summary"]

            if (
                "media" not in post["content"][0]
                and "media" in post["trail"][0]["content"][0]
            ):
                post["content"] = post["trail"][0]["content"]

            images = []
            for content in post["content"]:

                if content["type"] == "text":
                    text = content["text"]
                    continue
                elif content["type"] == "image":
                    image_url = None
                    for media in content["media"]:
                        if "cropped" in media:  # Skip cropped images
                            continue
                        response = requests.head(media["url"])
                        if not response.status_code == 200:
                            continue
                        if "has_original_dimensions" in media:
                            image_url = media["url"]
                            break
                    # If no image is marked as original, use the first
                    if not image_url:
                        images.append(CrawlerImage(content["media"][0]["url"]))
                    else:
                        images.append(CrawlerImage(image_url))
                else:
                    print("Unknown type: %s" % content["type"])

            if title:  # Add title to the first image
                images[0].title = title
            if text:  # Add text to the last image
                # Strip multi-byte characters
                images[-1].text = text.encode("ascii", errors="ignore").decode()

            return images

        if date and pub_date < date:  # If we are here, no post was found
            return self.crawl_posts(pub_date, page + 1)

    def crawl_helper(self, pub_date, blog_identifier):
        self.site = blog_identifier
        return self.crawl_posts(pub_date)