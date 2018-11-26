import os

from db import db
from flask import Flask, request, redirect, Response
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException

# from utils.parser import ReqParser

from views.RoomView import RoomView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///localdata.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)
"""
till here
"""
app.config['BASIC_AUTH_USERNAME'] = 'mark'
app.config['BASIC_AUTH_PASSWORD'] = 'mark'
basic_auth = BasicAuth(app)
admin = Admin(app, name="niche", template_mode='bootstrap3')
CORS(app)

if __name__ == '__main__':
    CORS(app)

@app.route('/hi')
def hello_world():
    return "running!"

@app.route('/checkroom', methods=['POST']) 
def check_room():
    return RoomView.check_room()

@app.route('/makeroom', methods=['POST']) 
def make_room():
    return RoomView.make_room()

@app.route('/makeentry', methods=['POST']) 
def make_room():
    return RoomView.make_entry()

@socketio.on('join')
def on_join(data):
    req_params = ["username", "room"]
    if not ReqParser.check_body(data, req_params):
        emit('error', {"error_message": 'invalid params'}, json=True)
    username = data['username']
    room = data['room']
    error, status = RoomController.check_room(room)
    if error:
        emit("error", error)
    join_room(room)
    error, status = RoomController.join_room(room, username)
    if error:
        emit("error", error)
    error, entries = EntryController.for_room(room)
    if error:
        emit("error", error)
    print('hi')
    emit("joined_room", entries)

@socketio.on('new_entry')
def on_new_entry(data):
    req_params = ["username", "room"]
    if not ReqParser.check_body(data, req_params):
        emit('error', {"error_message": 'invalid params'}, json=True)
    username = data['username']
    room = data['room']
    error, status = RoomController.check_room(room)
    if error:
        emit("error", error)
    error, entry = EntryController.new_entry(room, username)
    if error:
        emit("error", error)
    emit("got_new", entry, room=room)

# @socketio.on('leave')
# def on_leave(data):
#     req_params = ["username", "room"]
#     if not ReqParser.check_body(data, req_params):
#         emit('error', {"error_message": 'invalid params'}, json=True)
#     username = data['username']
#     room = data['room']
#     leave_room(room)
#     delete user by username
from models.MemberModel import MemberModel
from models.EntryModel import EntryModel
from models.RoomModel import RoomModel

class ModelView(sqla.ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True
    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

class EntryAdminView(ModelView):
    column_list = ['id', 'member', 'room']
    column_filters = ['id', 'member', 'room']
    column_default_sort = ('id', True)

class MemberAdminView(ModelView):
    column_list = ['id', 'name', 'room', 'privilege']
    column_filters = ['id', 'name', 'room']
    column_default_sort = ('id', True)

class RoomAdminView(ModelView):
    column_list = ['id', 'name']
    column_filters = ['id', 'name']
    column_default_sort = ('id', True) 

admin.add_view(EntryAdminView(EntryModel, db.session))
admin.add_view(MemberAdminView(MemberModel, db.session))
admin.add_view(RoomAdminView(RoomModel, db.session))


if __name__ == '__main__':
    db.init_app(app)
    @app.before_first_request
    def create_tables():
        db.create_all()
    socketio.run(app)