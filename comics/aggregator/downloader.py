import contextlib
import hashlib
import httplib
import mimetypes
import socket
import tempfile
import urllib2

try:
    from PIL import Image as PILImage
except ImportError:
    import Image as PILImage

from django.conf import settings
from django.core.files import File
from django.db import transaction

from comics.aggregator.exceptions import (DownloaderError, FileNotAnImage,
    DownloaderHTTPError, ImageTypeError, ImageIsCorrupt, ImageAlreadyExists,
    ImageIsBlacklisted)
from comics.core.models import Release, Image


class ReleaseDownloader(object):
    def download(self, crawler_release):
        images = self._download_images(crawler_release)
        return self._create_new_release(
            crawler_release.comic, crawler_release.pub_date, images)

    def _download_images(self, crawler_release):
        images = []
        for crawler_image in crawler_release.images:
            image_downloader = ImageDownloader(crawler_release)
            image = image_downloader.download(crawler_image)
            images.append(image)
        return images

    @transaction.commit_on_success
    def _create_new_release(self, comic, pub_date, images):
        release = Release(comic=comic, pub_date=pub_date)
        release.save()
        for image in images:
            release.images.add(image)
        return release


class ImageDownloader(object):
    def __init__(self, crawler_release):
        self.comic = crawler_release.comic
        self.pub_date = crawler_release.pub_date
        self.has_reruns = crawler_release.has_rerun_releases
        self.file_handle = None
        self.file_extension = None
        self.file_checksum = None

    @property
    def identifier(self):
        identifier = '%s/%s' % (self.comic.slug, self.pub_date)
        if self.file_checksum:
            identifier = '%s/%s' % (identifier, self.file_checksum[:6])
        return identifier

    @property
    def file_name(self):
        if self.file_checksum and self.file_extension:
            return '%s%s' % (self.file_checksum, self.file_extension)

    def download(self, crawler_image):
        self._download_image(crawler_image.url, crawler_image.request_headers)
        self._check_if_blacklisted(self.file_checksum)
        existing_image = self._get_existing_image(self.file_checksum)
        if existing_image is not None:
            return existing_image
        self._check_if_corrupt(self.file_handle)
        return self._create_new_image(crawler_image.title, crawler_image.text)

    def _download_image(self, url, request_headers):
        try:
            request = urllib2.Request(url, None, request_headers)
            with contextlib.closing(urllib2.urlopen(request)) as http_file:
                self._check_image_mime_type(http_file)
                self.file_extension = self._get_file_extension(http_file)
                self._check_known_image_type(self.file_extension)
                self.file_handle = self._get_temporary_file(http_file)
                self.file_checksum = self._get_sha256sum(self.file_handle)
        except urllib2.HTTPError as error:
            raise DownloaderHTTPError(self.identifier, error.code)
        except urllib2.URLError as error:
            raise DownloaderHTTPError(self.identifier, error.reason)
        except httplib.BadStatusLine:
            raise DownloaderHTTPError(self.identifier, 'BadStatusLine')
        except socket.error as error:
            raise DownloaderHTTPError(self.identifier, error)

    def _check_if_blacklisted(self, checksum):
        if checksum in settings.COMICS_IMAGE_BLACKLIST:
            raise ImageIsBlacklisted(self.identifier)

    def _get_existing_image(self, checksum):
        try:
            image = Image.objects.get(comic=self.comic, checksum=checksum)
            if image is not None and not self.has_reruns:
                raise ImageAlreadyExists(self.identifier)
            return image
        except Image.DoesNotExist:
            return None

    def _check_if_corrupt(self, file_handle):
        image = PILImage.open(file_handle)
        try:
            image.load()
        except IndexError:
            raise ImageIsCorrupt(self.identifier)
        except IOError as error:
            raise ImageIsCorrupt(self.identifier, error.message)

    @transaction.commit_on_success
    def _create_new_image(self, title, text):
        image = Image(comic=self.comic, checksum=self.file_checksum)
        image.file.save(self.file_name, File(self.file_handle))
        if title is not None:
            image.title = title
        if text is not None:
            image.text = text
        image.save()
        return image

    def _check_image_mime_type(self, http_file):
        if http_file.info().getmaintype() != 'image':
            raise FileNotAnImage(self.identifier)

    def _check_known_image_type(self, extension):
        if extension not in ('.gif', '.jpg', '.png'):
            raise ImageTypeError(self.identifier, extension)

    def _get_temporary_file(self, source_file):
        tmp = tempfile.NamedTemporaryFile(suffix='comics')
        tmp.write(source_file.read())
        tmp.seek(0)
        return tmp

    def _get_file_extension(self, http_file):
        mime_type = http_file.info().gettype()

        # MIME types like "image/jpeg, image/jpeg" have been observed.
        mime_type = mime_type.split(',')[0]

        # The MIME type "image/pjpeg" has been observed.
        mime_type = mime_type.replace('pjpeg', 'jpeg')

        file_ext = mimetypes.guess_extension(mime_type)
        if file_ext == '.jpe':
            file_ext = '.jpg'
        if file_ext is None:
            raise DownloaderError(self.identifier,
                'File extension not found: %s' % mime_type)
        return file_ext

    def _get_sha256sum(self, file_handle):
        original_position = file_handle.tell()
        hash = hashlib.sha256()
        while True:
            data = file_handle.read(8096)
            if not data:
                break
            hash.update(data)
        file_handle.seek(original_position)
        return hash.hexdigest()
