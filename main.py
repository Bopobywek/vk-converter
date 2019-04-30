import os
import logging

from flask import Flask, request, send_file
from config import CONFIRMATION_TOKEN
from system_function import create_files, USER_FILES_DIRCTORY
from dialog_handler import DialogHandler

app = Flask(__name__)
create_files()
dialog = DialogHandler(version=5.95)

logging.basicConfig(filename='converter.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s', level=logging.ERROR)


@app.route('/', methods=['POST'])
def processed():
    data = request.json
    if data.get('type', None) is None:
        return 'not vk'
    elif data.get('type') == 'confirmation':
        return CONFIRMATION_TOKEN
    else:
        logging.info('Request: {}'.format(request))
        try:
            if data['type'] == 'message_new':
                dialog.handle_request(data)
                return 'ok'
        except Exception as e:
            logging.error('Error while working with user. Error: {}'.format(e))
            return 'ok'


@app.route('/download/<path:file>')
def download_path(file):
    if os.path.exists(file):
        logging.info('Sending file with path: {}'.format(file))
        return send_file(file, as_attachment=True)
    else:
        logging.error('File is not exists. Path: {}'.format(file))
        return '''<center><h1>Произошла ошибка. Файл не был найден.
         Пожалуйста, попробуйте ещё раз.</h1></center>'''


if __name__ == '__main__':
    app.run(port=8080)
