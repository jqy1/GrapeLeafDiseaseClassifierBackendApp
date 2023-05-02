import uuid,datetime
#from flask import current_app as app
from sqlalchemy_serializer import SerializerMixin
import jwt
from typing import Union

from flask import current_app as app

from .. import db,flask_bcrypt
from ..config import jwt_key, key
from flask import current_app as app


class Model(db.Model):
    """Model that can store training models.
       
    """

    # table name of MySQL database
    __tablename__ = 'u_model'

    id = db.Column(db.Integer, primary_key = True)
    model_type = db.Column(db.String(1024))
    date = db.Column(db.DateTime, nullable=True)
    file_path = db.Column(db.String(120))
    version = db.Column(db.String(32))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'model_type': self.model_type,
            'date': self.date,
            'file_path': self.file_path,
            'version': self.version
    }

    @staticmethod
    def serialize_list(l):
        return [ m.serialize for m in l ]

    def __repr__(self):
        return "<Model '{}'>".format(self.id,self.model_type,self.date,self.file_path, self.version)



