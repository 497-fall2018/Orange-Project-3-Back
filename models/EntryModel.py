from db import db
from datetime import datetime

from models.basemodel import BaseModel

class EntryModel(db.Model, BaseModel):
    __tablename__ = "entry"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    room = db.Column(db.Integer, db.ForeignKey('room.id'))
    member = db.Column(db.String(255))

    def __init__(self, member, room):
        self.member = member
        self.room = room

    def json(self):
        return {
            "id": self.id,
            "room": self.room,
            "member": self.member,
        }

    @classmethod
    def find_by_member(cls, member):
        return cls.query.filter_by(member=member).first()
    @classmethod
    def filter_by_room(cls, room):
        return cls.query.filter_by(room=room).all()
