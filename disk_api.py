import os

import yadisk

from config import YANDEX_DISK_TOKEN


class YandexDiskHandler(object):

    def __init__(self, path, local_filename, origin_filename):
        self.path = path
        self.local_filename = local_filename
        self.origin_filename = origin_filename
        self.original_path_to_file = os.path.join(path, local_filename)
        self.yandex_api = yadisk.YaDisk(token=YANDEX_DISK_TOKEN)

    def upload_publish_file(self):
        self.yandex_api.upload(self.original_path_to_file, self.origin_filename, overwrite=True)
        return self.yandex_api.get_download_link(path=self.origin_filename)

    def remove_from_disk(self):
        self.yandex_api.remove(self.origin_filename)


if __name__ == '__main__':
    pass
