import uuid,datetime
from sqlalchemy_serializer import SerializerMixin
import jwt
from typing import Union

from flask import current_app as app

from .. import db,flask_bcrypt
from ..config import jwt_key, key
from flask import current_app as app


class Result(db.Model):
    """
    Result that can store the classification result. 
    """

    # table name of MySQL database
    __tablename__ = 'u_result'

    id = db.Column(db.Integer, primary_key = True)
    uri = db.Column(db.String(1024))
    disease = db.Column(db.String(120))
    possibility = db.Column(db.String(128))
    user_id = db.Column(db.String(100))
    date = db.Column(db.DateTime, nullable=True)
    file_path = db.Column(db.String(120))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'uri': self.uri,
            'disease': self.disease,
            'possibility': self.possibility,
            'user_id': self.user_id,
            'date': str(self.date),
            'file_path': self.file_path
    }

    @staticmethod
    def serialize_list(l):
        return [ m.serialize for m in l ]

    def __repr__(self):
        return "<Result '{}'>".format(self.id,self.uri,self.file_path,self.disease )