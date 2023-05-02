import uuid,datetime
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from typing import Dict, Tuple
from ..models.Result import Result as Result
from .. import db
from ..config import jwt_key, key



class ResultService(object):
    """
        UserService class allows to create, update, delete, get, and get_all users from databse
    """
    def __init__(self):
        pass

    @staticmethod
    def get_all():
        users = Result.query.all()
        print(users)
        if len(users) :
            return User.serialize_list(users)
        return None

    @staticmethod
    def get(result_id):
        result = Result.query.get(result_id)
        if result is None:
            return None
        return result.serialize

    @staticmethod
    def create(data: Dict[str, str]):
        app.logger.info('%s successfully invoke ResultService', "save")
        result = Result.query.filter_by(mail=data['uri']).first()
        if not result:
            new_result = Result(
                id=str(uuid.uuid4()),
                uri = data['uri'],
                disease = data['disease'],
                possibility = data['possibility'],
                user_id = data['user_id'],
                date =datetime.datetime.utcnow(),
                file_path = data['file_path']

            )
            ResultService.save_changes(new_result)
            return new_result.id, 200 
        else:
            return "fail", 201

    @staticmethod
    def save_changes(data: Result, add_or_edit = False) -> None:
        if add_or_edit:
            data.verified = True
        db.session.add(data)
        db.session.commit()

    @staticmethod
    def update(self, result_id, result : Result):
        app.logger.info('%s successfully invoke ResultService', "update")
        ResultService.save_changes(result,add_or_edit = True)
        return result.id

    @staticmethod
    def delete(self, result_id):
        result = Result.query.get(result_id)
        if result is not None and isinstance(result, Result):
            db.session.delete(result)
            db.session.commit()
            return result.id, 200
        app.logger.info('%s successfully invoke ResultService', "delete")
        return id, 404