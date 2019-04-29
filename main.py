import os
from urllib import parse
from random import randint

import vk
from flask import Flask, request

from config import CONFIRMATION_TOKEN, TOKEN
from system_function import create_folder, USER_FILES_DIRCTORY, create_files, get_file_type
from dialog_handler import DialogHandler

app = Flask(__name__)
create_files()
dialog = DialogHandler(version=5.95)


@app.route('/', methods=['POST'])
def processed():
    data = request.json
    if data.get('type', None) is None:
        return 'not vk'
    elif data.get('type') == 'confirmation':
        return CONFIRMATION_TOKEN
    else:
        if data['type'] == 'message_new':
            dialog.handle_request(data)
            return 'ok'


if __name__ == '__main__':
    app.run(port=8080)
