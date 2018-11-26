import json
from flask import request

from utils.parser import ReqParser
from controllers.RoomController import RoomController

class RoomView:
    @classmethod
    def check_room(cls):
        data = json.loads(request.data.decode('utf-8'))
        req_params = ['roomcode']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status = RoomController.check_room(data['roomcode'])

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success"}), status

    @classmethod
    def make_room(cls):
        data = json.loads(request.data.decode('utf-8'))
        req_params = ['roomcode', 'username']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status = RoomController.make_room(data['roomcode'], data['username'])

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success"}), status
