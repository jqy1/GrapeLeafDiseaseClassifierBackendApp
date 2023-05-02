import uuid,datetime
from sqlalchemy_serializer import SerializerMixin
import jwt
from typing import Union

from flask import current_app as app

from .. import db,flask_bcrypt
from ..config import jwt_key, key
from flask import current_app as app


class User(db.Model):
    """User that can use this system. It maps to a table in MySQL Database.
       
    """

    # table name of MySQL database
    __tablename__ = 'u_users'

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(120))
    sur_name = db.Column(db.String(120))
    mail = db.Column(db.String(256))
    password_hash = db.Column(db.String(100))
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Integer, nullable=False, default='1')
    public_id = db.Column(db.String(100), unique=False)
    user_name = db.Column(db.String(50), unique=True)
    user_level = db.Column(db.String(50), unique=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'sur_name': self.sur_name,
            'mail': self.mail,
            'password_hash': self.password_hash,
            'registered_on': str(self.registered_on),
            'admin': self.admin,
            'public_id': self.public_id,
            'user_name': self.user_name,
            'user_level': self.user_level
    }

    @staticmethod
    def serialize_list(l):
        return [ m.serialize for m in l ]

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        # generate a password based on user's input and salt.
        self.password_hash = flask_bcrypt.generate_password_hash( password + "&" + key).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password + "&" + key )
    
    @staticmethod
    def encode_auth_token(user_id: int) -> bytes:
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                jwt_key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token: str) -> Union[str, int]:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, jwt_key,algorithms='HS256')
            app.logger.info('payload -> %s', payload)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User '{}'>".format(self.user_name)

    