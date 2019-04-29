from flask import Flask, request

from config import TOKEN, CONFIRMATION_TOKEN


app = Flask(__name__)
user_sessions = dict()


@app.route('/', methods=['POST'])
def processed():
    data = request.json
    if data.get('type', None) is None:
        return 'not vk'
    elif data.get('type') == 'confirmation':
        return CONFIRMATION_TOKEN
    else:
        user_id = data['object']['peer_id']
        if user_id in user_sessions:
            pass
        else:
            pass


