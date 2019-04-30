import os
from urllib import parse
import requests
import logging

from werkzeug.utils import secure_filename
from config import YANDEX_DISK_DOWNLOAD_URL, GOOGLE_DRIVE_DOWNLOAD_URL

MAX_CONTENT_LENGTH = 400 * 1024 * 1024

logging.basicConfig(filename='converter.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s', level=logging.ERROR)


def get_filename(field, type_of_disk):
    if type_of_disk == 'google':
        filename = field.split(';')[2]
        return secure_filename(filename[filename.rfind("'") + 1:])
    else:
        filename = field.split(';')[1]
        return secure_filename(filename[filename.rfind("'") + 1:])


class YandexDiskDownloader(object):

    def __init__(self, public_key):
        self.public_key = public_key

    def get_link_on_file(self):
        params = {
            'public_key': self.public_key
        }
        return requests.get(YANDEX_DISK_DOWNLOAD_URL, params=params).json()

    def download_file(self, path):
        try:
            data = self.get_link_on_file()
            if isinstance(data, dict):
                if 'href' in data:
                    href = data.get('href')
                    if int(requests.head(href).headers.get('Content-Length')) <= MAX_CONTENT_LENGTH:
                        result = requests.get(href)
                        logging.info('request yo disk Yandex: {}'.format(result))
                        filename = get_filename(result.headers.get('Content-Disposition'), type_of_disk='yandex')
                        file = result.content
                        with open(os.path.join(path, filename), mode='wb') as fout:
                            fout.write(file)
                        return dict(filename=filename, file=file)
        except Exception as e:
            logging.error(e)
            return dict()


class GoogleDriveDownloader(object):

    def __init__(self, url):
        self.url = url

    def parse_link_to_id(self):
        return parse.parse_qs(parse.urlsplit(self.url).query).get('id')[0]

    def download_file(self, path):
        try:
            params = {
                'export': 'download',
                'id': self.parse_link_to_id()
            }
            logging.info('request to Google Drive with id: {}'.format(params.get('id')))
            result = requests.get(GOOGLE_DRIVE_DOWNLOAD_URL, params=params)
            filename = get_filename(result.headers.get('Content-Disposition'), type_of_disk='google')
            file = result.content
            with open(os.path.join(path, filename), mode='wb') as fout:
                fout.write(file)
            return dict(filename=filename, file=file)
        except Exception as e:
            logging.error(e)
            return dict()


RESOURCES = {'yadi.sk': YandexDiskDownloader, 'drive.google.com': GoogleDriveDownloader}


if __name__ == '__main__':
    pass
