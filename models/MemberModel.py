from db import db
from datetime import datetime

from models.basemodel import BaseModel

class MemberModel(db.Model, BaseModel):
    __tablename__ = "member"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    name = db.Column(db.String(255))

    privilege = db.Column(db.Integer)
    room = db.Column(db.Integer, db.ForeignKey('room.id'))

    def __init__(self, name, privilege, room):
        self.name = name
        self.privilege = privilege
        self.room = room
        

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
