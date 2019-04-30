from flask import Flask, request, send_file
from config import CONFIRMATION_TOKEN
from system_function import create_files, USER_FILES_DIRCTORY
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


@app.route('/download/<path:file>')
def download_path(file):
    return send_file(file, as_attachment=True)


if __name__ == '__main__':
    app.run(port=8080)
