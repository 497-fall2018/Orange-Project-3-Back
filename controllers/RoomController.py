from models.RoomModel import RoomModel
from models.MemberModel import MemberModel

class RoomController:
    @classmethod
    def make_room(cls):
        pass
    @classmethod
    def check_room(cls, roomcode):
        target = RoomModel.find_by_name(roomcode)
        if target:
            return "", 200
        else:
            return "Unknown Room Code", 400

