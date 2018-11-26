from models.RoomModel import RoomModel
from models.MemberModel import MemberModel
from models.EntryModel import EntryModel

class EntryController:
    @classmethod
    def for_room(cls, roomcode):
        target = RoomModel.find_by_name(roomcode)
        if target:
            all_entries = EntryModel.filter_by_room(target.id)
            return '', list(map(lambda x : x.json() if x else None, all_entries))
        else:
            return "Invalid Room Name", None

    @classmethod
    def new_entry(cls, roomcode, username):
        target = RoomModel.find_by_name(roomcode)
        if target:
            new_entry = EntryModel(username, target.id)
            new_entry.save_to_db()
            return '', new_entry.json()
        else:
            return "Invalid Room Name", None

