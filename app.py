import json

import bson
from bson import ObjectId
from flask import Flask
from flask_mongoengine import MongoEngine
from werkzeug.exceptions import BadRequest
from flask import jsonify, request
import jwt
from controller import *
import requests

app = Flask(__name__)
app.config['MONGODB_DB'] = 'Portal'
app.config[
    'MONGODB_HOST'] = 'mongodb://admin_odko:WinniePooh@portalinternational-shard-00-00-3b6lw.mongodb.net:27017,portalinternational-shard-00-01-3b6lw.mongodb.net:27017,portalinternational-shard-00-02-3b6lw.mongodb.net:27017/Portal?ssl=true&replicaSet=PortalInternational-shard-0&authSource=admin'
app.config['MONGODB_USERNAME'] = 'admin_odko'
app.config['MONGODB_PASSWORD'] = 'WinniePooh'
db = MongoEngine()
db.init_app(app)

USER_API_URL = 'http://127.0.0.1:5000/user'

@app.route('/api/chat/users/<string:user1>/<string:user2>', methods=['GET', 'POST'])
def chat_users(user1, user2):
    if request.method == 'GET':
        conv = get_chat([ObjectId(user1), ObjectId(user2)])
        if conv:
            return jsonify({'response': conv,
                            'statusCode': 200}), 200
        else:
            conv = create_chat(users=[ObjectId(user1), ObjectId(user2)])
            return jsonify({'response': conv,
                            'statusCode': 200}), 200
    elif request.method == 'POST':
        conv = create_chat([ObjectId(user1), ObjectId(user2)])
        return jsonify({'response': conv,
                        'statusCode': 200}), 200


@app.route('/api/chat/user/<string:user1>')
def chat_user(user1):
    if request.method == 'GET':
        payload = request.json
        limit = payload.get('limit', 10)
        skip = payload.get('skip', 0)

        chats = json.loads(get_chats_user(user1, skip, limit).to_json())
        print(chats)

        return jsonify({'response': chats,
                            'statusCode': 200}), 200


@app.route('/api/chat/<string:chat_id>', methods=['GET'])
def chat(chat_id):
    if request.method == 'GET':
        conv = get_chat_by_id(ObjectId(chat_id)).to_json()
        if conv:
            return jsonify({'response': json.loads(conv.to_json),
                            'statusCode': 200}), 200
        else:
            return jsonify({'response': [],
                            'statusCode': 200}), 200


@app.route('/api/chat/<string:chat_id>/user/<string:user_id>', methods=['POST'])
def add_chat(chat_id, user_id):
    if request.method == 'POST':
        if is_valid_id(chat_id) and is_valid_id(user_id):
            body = request.json['body']
            created_when = request.json.get('created_when')
            created_when = datetime.datetime.fromtimestamp(created_when/100.0)
            message = add_message(chat_id, user_id, body, created_when)
            return jsonify({'response':message,
                            'statusCode': 200}), 200
        else:
            raise BadRequest


@app.route('/api/chat/<string:chat_id>/message')
def get_msgs(chat_id):
    if request.method == 'GET':
        fields = request.json.get('fields', [])
        message = get_all_messages(ObjectId(chat_id), fields).to_json()
        return jsonify({'response':json.loads(message),
                        'statusCode': 200}), 200


@app.route('/api/chat/user/<string:user_id>/message')
def get_chats_by_user(user_id):
    if request.method == 'GET':
        message = get_all_chats(ObjectId(user_id)).to_json()
        return jsonify({'response':json.loads(message),
                        'statusCode': 200 }), 200


@app.errorhandler(BadRequest)
def global_handler_bad_request(e):
    print(e)
    return jsonify({'statusCode': 401, 'response': str(e)}), 401


@app.errorhandler(bson.errors.InvalidId)
def global_handler_not_found(e):
    return jsonify({'statusCode': 404, 'response': 'Not found'}), 404


def is_valid_id(_id):
    return len(_id)==24 and _id is not None

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
