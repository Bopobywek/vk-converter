import os
import shutil
from pathlib import Path

from convert_functions import VIDEO_SUPPORTED_FORMATS, AUDIO_SUPPORTED_FORMATS, PICTURE_SUPPORTED_FORMATS

USER_FILES_DIRCTORY = 'files/'


def create_folder(name):
    if os.path.exists(os.path.join(USER_FILES_DIRCTORY, name)):
        delete_folder(name)
    os.mkdir(os.path.join(USER_FILES_DIRCTORY, name))
    return os.path.join(USER_FILES_DIRCTORY, name)


def delete_folder(name):
    path = os.path.join(USER_FILES_DIRCTORY, name)
    if os.path.exists(path):
        shutil.rmtree(os.path.join(USER_FILES_DIRCTORY, name))


def create_files():
    if not os.path.exists(USER_FILES_DIRCTORY):
        os.mkdir(USER_FILES_DIRCTORY)


def get_file_type(file):
    suf = Path(file).suffix[1:].upper()
    if suf in AUDIO_SUPPORTED_FORMATS:
        return AUDIO_SUPPORTED_FORMATS
    elif suf in PICTURE_SUPPORTED_FORMATS:
        return PICTURE_SUPPORTED_FORMATS
    elif suf in VIDEO_SUPPORTED_FORMATS:
        return VIDEO_SUPPORTED_FORMATS
