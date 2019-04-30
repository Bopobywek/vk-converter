import json
import os
from urllib import parse
from random import randint
import logging

import vk

from downloader_from_disks import RESOURCES
from system_function import USER_FILES_DIRCTORY, delete_folder, create_folder, get_file_type
from convert_functions import Converter
from config import TOKEN

user_sessions = dict()

HOST = 'http://benjamingg.pythonanywhere.com'

logging.basicConfig(filename='converter.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s', level=logging.ERROR)


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
                logging.info('New user added. Peer_id: {}'.format(peer_id))
                self.upsert_user_in_session(peer_id, list())
            msg = self.generate_message(peer_id, request)
            logging.info('New message was generated. Message: {}'.format(msg))
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

    def generate_message(self, peer_id, request):
        result = self.find_link_in_request(request)
        if result is not None:
            create_folder(str(peer_id))
            logging.info('Directory created: {}'.format(str(peer_id)))
            downloader = result[0](result[1])
            file_info = downloader.download_file(os.path.join(USER_FILES_DIRCTORY, str(peer_id)))
            types_allowed = get_file_type(file_info.get('filename'))
            if types_allowed is None:
                message = 'Извините, но я не умею конвертировать файлы данного формата'
                return dict(message=message)
            self.upsert_user_in_session(peer_id, types_allowed)
            keyboard = self.create_keyboard(types_allowed)
            message = 'Пожалуйста, укажите на клавиатуре формат, в который вы хотите сконвертировать файл. ' \
                      'После начнется конвертация. Она займет некоторое время.'
            return dict(keyboard=keyboard, message=message)
        else:
            logging.info('Users suggest: {}'.format(self.user_get_suggest(peer_id)))
            if request.get('object', dict()).get('text', None) in self.user_get_suggest(peer_id):
                path = os.path.join(USER_FILES_DIRCTORY, str(peer_id))
                directory = os.listdir(path)
                if bool(directory):
                    filename = directory[0]
                else:
                    logging.error('File not found. Dir: {}'.format(directory))
                    return dict(message='Извините, возникла ошибка. Файл не найден.')
                converter = Converter(path=path,
                                      filename=filename,
                                      new_format=request.get('object', dict()).get('text'))
                res = converter.convert()
                self.delete_user_suggest(peer_id)
                if bool(res):
                    for e in res:
                        logging.error(e)
                    delete_folder(str(peer_id))
                    return dict(message='Извините, возникла ошибка при конвертации, попробуйте ещё раз.')
                return dict(message='Ссылка на скачивание: {}'.format('{}/download/{}'.format(HOST,
                                                                                              converter.new_file_path)))
            else:
                if bool(self.user_get_suggest(peer_id=peer_id)):
                    keyboard = self.create_keyboard(self.user_get_suggest(peer_id))
                    message = 'Пожалуйста, выберите на клавиатуре формат, в который вы хотите сконвертировать файл'
                    return dict(keyboard=keyboard, message=message)
                else:
                    message = 'Пожалуйста, отправьте ссылку на файл'
                    return dict(message=message)

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
            return user_sessions[peer_id]

    def delete_user_suggest(self, peer_id):
        if self.user_in_session(peer_id):
            if self.with_db:
                pass
            del user_sessions[peer_id]

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
                link = attachments[0].get('link', '').get('url', '')
                result = self.is_allowed_url(link)
                if result is not None:
                    return result, link
