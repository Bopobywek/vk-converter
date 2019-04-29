import os
import shutil
from pathlib import Path

ARCHIVE_CONTENT_FOLDER = 'content'
ARCHIVE_SUPPORTED_FORMATS = [x[0] for x in shutil.get_unpack_formats()]
SUFFIXES_TO_FORMAT = {x[0]: x[1] for x in shutil.get_unpack_formats()}
FORMAT_TO_SUFFIXES = {s: x for x, y in SUFFIXES_TO_FORMAT.items() for s in y}
SUPPORTED_SUFFIXES = list(FORMAT_TO_SUFFIXES.keys())
SUPPORTED_ARCHIVE_FORMATS_FOR_FORMS = {x: x.split('.')[-1] for x in SUPPORTED_SUFFIXES}


class ArchiveFuncs(object):

    def __init__(self, path, filename):
        self.path = path
        self.original_file = os.path.join(path, filename)
        self.suffix = Path(filename).suffix
        if self.suffix:
            self.filename = filename[:filename.find(self.suffix)]
        else:
            self.filename = filename

    def extract_archive(self):
        try:
            directory = os.path.join(self.path, ARCHIVE_CONTENT_FOLDER)
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.mkdir(directory)
            shutil.unpack_archive(self.original_file, directory, FORMAT_TO_SUFFIXES.get(self.suffix))
        except Exception as e:
            return 'error', e

    def make_archive(self, arc_format):
        try:
            filename = shutil.make_archive(os.path.join(self.path, self.filename),
                                           arc_format, os.path.join(self.path, ARCHIVE_CONTENT_FOLDER))
            return '/'.join(filename.split('/')[-3:])
        except Exception as e:
            return 'error', e

    def all_files(self):
        content_of_dir = dict(dirs=list(), files_full=list(), files=list())
        for root, dirs, files in os.walk(os.path.join(self.path, ARCHIVE_CONTENT_FOLDER)):
            content_of_dir['dirs'].extend(dirs)
            for file in files:
                content_of_dir['files'].append((os.path.join(root, file),
                                                '/'.join(os.path.join(root, file).split('/')[3:])))
        return content_of_dir, '{}{}'.format(self.filename, self.suffix)


if __name__ == '__main__':
    print(ARCHIVE_SUPPORTED_FORMATS)
