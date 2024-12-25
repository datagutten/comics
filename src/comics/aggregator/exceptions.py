from comics.core.exceptions import ComicsError


class AggregatorError(ComicsError):
    """base class for aggregator exceptions"""

    def __init__(self, identifier, value=None):
        self.identifier = identifier
        self.value = value

    def __str__(self):
        return "%s: Generic aggregator error" % self.identifier


###


class CrawlerError(AggregatorError):
    """Base class for crawler exceptions"""

    def __str__(self):
        return f"{self.identifier}: Generic crawler error ({self.value})"


class CrawlerHTTPError(CrawlerError):
    """Exception used to wrap HTTP errors from the crawler"""

    def __str__(self):
        return f"{self.identifier}: Crawler HTTP Error ({self.value})"


class ImageURLNotFound(CrawlerError):
    """Exception raised when no URL is found by the crawler"""

    def __str__(self):
        return "%s: Image URL not found" % self.identifier


class NotHistoryCapable(CrawlerError):
    """Exception raised when a comic is not history capable for the date"""

    def __str__(self):
        return f"{self.identifier}: Comic is not history capable ({self.value})"


class ReleaseAlreadyExists(CrawlerError):
    """Exception raised when crawling a release that already exists"""

    def __str__(self):
        return "%s: Release already exists" % self.identifier


###


class DownloaderError(AggregatorError):
    """Base class for downloader exceptions"""

    def __str__(self):
        return f"{self.identifier}: Generic downloader error ({self.value})"


class DownloaderHTTPError(DownloaderError):
    """Exception used to wrap HTTP errors from the downloader"""

    def __str__(self):
        return f"{self.identifier}: Downloader HTTP Error ({self.value})"


class ImageTypeError(DownloaderError):
    """Exception raised when the image isn't of the right type"""

    def __str__(self):
        return f"{self.identifier}: Invalid image type ({self.value})"


class ImageIsCorrupt(DownloaderError):
    """Exception raised when the fetched image is corrupt"""

    def __str__(self):
        return f"{self.identifier}: Image is corrupt ({self.value})"


class ImageAlreadyExists(DownloaderError):
    """Exception raised when trying to save an image that already exists"""

    def __str__(self):
        return "%s: Image already exists" % self.identifier


class ImageIsBlacklisted(DownloaderError):
    """Exception raised when a blacklisted image has been downloaded"""

    def __str__(self):
        return "%s: Image is blacklisted" % self.identifier
