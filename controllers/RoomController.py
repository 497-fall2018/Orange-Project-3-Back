from models.RoomModel import RoomModel
from models.MemberModel import MemberModel

class RoomController:
    @classmethod
    def check_room(cls, roomcode):
        target = RoomModel.find_by_name(roomcode)
        if target:
            return "", 200
        else:
            return "Unknown Room Code", 400
    
    @classmethod
    def make_room(cls, roomcode, username):
        target = RoomModel.find_by_name(roomcode)
        if target:
            return "Room already exists with that name", 400
        else:
            new_room = RoomModel(roomcode)
            new_room.save_to_db()
            new_member = MemberModel(username, 100, new_room.id)
            new_member.save_to_db()
            return "", 200

    @classmethod
    def join_room(cls, roomcode, username):
        target = RoomModel.find_by_name(roomcode)
        if target:
            new_member = MemberModel(username, 1, target.id)
            new_member.save_to_db()
            return "", 200
        else:
            return "Invalid Room Name", 400


