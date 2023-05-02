import uuid,datetime
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from typing import Dict, Tuple
from ..models.User import User as User
from .. import db
from ..config import jwt_key, key



class UserService(object):
    """
        UserService class allows to create, update, delete, get, and get_all users from databse
    """
    def __init__(self):
        pass

    @staticmethod
    def get_all():
        users = User.query.all()
        print(users)
        if len(users) :
            return User.serialize_list(users)
        return None

    @staticmethod
    def get(user_id):
        user = User.query.get(user_id)
        if user is None:
            return None
        return user.serialize

    @staticmethod
    def create(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        app.logger.info('%s successfully invoke UserService', "save")
        user = User.query.filter_by(mail=data['mail']).first()
        if not user:
            new_user = User(
                public_id=str(uuid.uuid4()),
                first_name = data['first_name'],
                sur_name = data['sur_name'],
                mail = data['mail'],
                password = data['password_hash'],
                admin = data['admin']  if 'admin' in data else 0,
                user_level = data['user_level'] if 'user_level' in data else "Normal",                
                user_name = data['user_name'],
                registered_on=datetime.datetime.utcnow(),

            )
            UserService.save_changes(new_user)
            auth_token, code = UserService.generate_token(new_user)
            #app.logger.info( ('successfully invoke UserService to generate token {} {}').format(auth_token, code))
            response = { 
                'code': code,
                'message':'succeed',
                'data': {
                    "Authorization": auth_token
                }  
            }
            return response, code
        else:
            response = { 
                'code': 201,
                'message':'Already exist, please login in or reset new password',
                'data': {
                    "Authorization": "fail"
                }  
            }
            return response, 201

    @staticmethod
    def save_changes(data: User, add_or_update=False) -> None:
        if add_or_update:
            data.verified = True
        db.session.add(data)
        db.session.commit()

    @staticmethod
    def update(self, user_id, user : User):
        app.logger.info('%s successfully invoke UserService {}', "update",user)
        UserService.save_changes(data = user,add_or_update = True)
        return user.id

    @staticmethod
    def delete(self, user_id):
        result = User.query.get(user_id)
        if result is not None and isinstance(result, User):
            db.session.delete(result)
            db.session.commit()
            return result.id, 200
        app.logger.info('%s successfully invoke UserService {}', "delete",result)
        return id, 404


    @staticmethod
    def generate_token(user: User) -> Tuple[Dict[str, str], int]:
        auth_token = User.encode_auth_token(user.id)
        if auth_token and len(auth_token) > 0: 
            return auth_token, 200
        return "", 401
