
import uuid,datetime
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from typing import Dict, Tuple
from ..models.Model import Model as Model
from .. import db
from ..config import jwt_key, key



class ModelService(object):
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
    def create(data: Dict[str, str]):
        app.logger.info('%s successfully invoke ModelService {}', "save", data)
        user = Model.query.filter_by(mail=data['mail']).first()
        if not user:
            new_user = User(
                model_type = data['model_type'],
                file_path = data['file_path'],
                version = data['version'],
                date=datetime.datetime.utcnow(),

            )
            UserService.save_changes(new_user)
            return UserService.generate_token(new_user)
        else:
            return "fail", 201

    @staticmethod
    def save_changes(data: Model, add_or_update:False) -> None:
        if add_or_edit:
            data.verified = True
        db.session.add(data)
        db.session.commit()

    @staticmethod
    def update(self, user_id, model : Model):
        app.logger.info('%s successfully invoke UserService {}', "update",model)
        ModelService.save_changes(result,True)
        return user.id

    @staticmethod
    def delete(self, user_id):
        result = Model.query.get(user_id)
        if result is not None and isinstance(result, Model):
            db.session.delete(result)
            db.session.commit()
            return result.id, 200
        app.logger.info('%s successfully invoke UserService {}', "delete",result)
        return id, 404