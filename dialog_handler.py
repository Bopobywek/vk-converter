import json
import os
from urllib import parse
from random import randint

import vk

from downloader_from_disks import RESOURCES
from system_function import USER_FILES_DIRCTORY, create_folder, get_file_type
from convert_functions import Converter
from config import TOKEN

user_sessions = dict()


class DialogHandler(object):

    def __init__(self, version, with_db=False):
        self.with_db = with_db
        session = vk.Session()
        self.api = vk.API(session, v=version)

    def handle_request(self, request):
        if not isinstance(request, dict):
            request = json.loads(request)
        if isinstance(request, dict):
            peer_id = self.get_peer_id(request)
            if not self.user_in_session(peer_id):
                self.upsert_user_in_session(peer_id, dict(suggests=[]))
            msg = self.generate_message(peer_id, self.user_get_suggest(peer_id), request)
            self.send_message(peer_id, message=msg.get('message'), keyboard=msg.get('keyboard', None))

    @staticmethod
    def get_peer_id(request):
        res = request.get('object', dict()).get('peer_id', None)
        if res is None:
            res = request.get('object', dict()).get('user_id', None)
        return res

    def send_message(self, peer_id, message, keyboard=None):
        if keyboard is not None:
            self.api.messages.send(peer_id=peer_id, access_token=TOKEN,
                                   message=message, keyboard=keyboard, random_id=randint(1, 10**10))
            return
        self.api.messages.send(peer_id=peer_id, access_token=TOKEN,
                               message=message, random_id=randint(1, 10**10))

    def generate_message(self, peer_id, suggests, request):
        if not bool(suggests):
            result = self.find_link_in_request(request)
            if result is None:
                return dict(message='Пожалуйста, отправьте ссылку на файл')
            create_folder(str(peer_id))
            downloader = result[0](result[1])
            file_info = downloader.download_file(os.path.join(USER_FILES_DIRCTORY, str(peer_id)))
            types_allowed = get_file_type(file_info.get('filename'))
            if types_allowed is None:
                message = 'Извините, но я не умею конвертировать файлы данного формата'
                return dict(message=message)
            self.upsert_user_in_session(peer_id, dict(suggests=types_allowed,
                                                      filename=file_info.get('filename')))
            keyboard = self.create_keyboard(types_allowed)
            message = 'Пожалуйста, выберите на клавиатуре формат, в который вы хотите сконвертировать файл'
            return dict(keyboard=keyboard, message=message)
        elif bool(suggests):
            if request.get('object', dict()).get('text') in self.user_get_suggest(peer_id):
                converter = Converter(path=os.path.join(USER_FILES_DIRCTORY, str(peer_id)),
                                      filename=self.user_get_filename(peer_id),
                                      new_format=request.get('object', dict()).get('text'))
                converter.convert()
                return dict(message='Конвертация прошла успешна')
            keyboard = self.create_keyboard(suggests)
            message = 'Пожалуйста, выберите на клавиатуре формат, в который вы хотите сконвертировать файл'
            return dict(keyboard=keyboard, message=message)

    @staticmethod
    def create_keyboard(array_of_bodies):
        buttons = list()
        buttons_on_line = list()
        for element in enumerate(array_of_bodies, start=1):
            button = {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': element[0]}),
                    'label': element[1],
                },
                'color': 'primary'
            }
            buttons_on_line.append(button)
            if element[0] % 4 == 0 or element[0] == len(array_of_bodies):
                buttons.append(buttons_on_line.copy())
                buttons_on_line.clear()
        keyboard = {
            'one_time': True,
            'buttons': buttons
        }
        return str(json.dumps(keyboard))

    def upsert_user_in_session(self, peer_id, suggest):
        if self.with_db:
            pass
        else:
            user_sessions[peer_id] = suggest

    def user_in_session(self, peer_id):
        if self.with_db:
            pass
        return peer_id in user_sessions

    def user_get_suggest(self, peer_id):
        if self.user_in_session(peer_id):
            if self.with_db:
                pass
            return user_sessions[peer_id].get('suggests')

    def user_get_filename(self, peer_id):
        if self.user_in_session(peer_id):
            if self.with_db:
                pass
            return user_sessions[peer_id].get('filename')

    @staticmethod
    def is_allowed_url(url):
        netloc_url = parse.urlsplit(url).netloc
        if netloc_url in RESOURCES.keys():
            return RESOURCES[netloc_url]
        return None

    def find_link_in_request(self, data):
        attachments = data.get('object', dict()).get('attachments')
        text = data.get('object', dict()).get('text')
        if text is not None and text != '':
            text = text.split()
            for el in text:
                result = self.is_allowed_url(el)
                if result is not None:
                    return result, el
        else:
            attachments = list(filter(lambda dictionary: dictionary.get('type') == 'link', attachments))
            if bool(attachments):
                link = attachments[0].get('link', '')
                result = self.is_allowed_url(link)
                if result is not None:
                    return result, link
