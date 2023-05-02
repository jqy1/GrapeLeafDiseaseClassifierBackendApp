from functools import wraps
from flask import request
from typing import Callable

from flask import current_app as app

from app.models.User import User as User
from app.service.AuthService import AuthService
from app import db
from app.config import jwt_key, key

from app.utils.parameter import validate_mail, validate_password


def token_required(f) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = request.headers.get('Authorization') 
        if not auth_token:
            response_object = {
                "code":"403",
                "message":"Authorization missed.",
                "data": {'Authorization':"fail"} 
            }
            return response_object, 403

        data, status = AuthService.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated


def register_valiation(f) -> Callable:
    """ a help function to validate the input register iinformation that must be accepted the password policy """
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.json
        if not data:
            response_object = {
                "code":"401",
                "message":"Missing paramaters.",
                "data": {'Authorization':"fail"} 
            }
            return response_object, 401

        mail = data['mail']

        if not mail:
            response_object = {
                "code":"401",
                "message":"Missing paramater mail or wrong format of mail.",
                "data": {'paramater':"mail"} 
            }
            return response_object, 401
        
        if not validate_mail(mail):
            response_object = {
                "code":"401",
                "message":"Mail must be a valid email address.",
                "data": {'paramater':"mail"} 
            }
            return response_object, 401


        password = data['password_hash']

        if not password:
            response_object = {
                "code":"401",
                "message":"Missing paramater password or wrong format of password.",
                "data": {'paramater':"password"} 
            }
            return response_object, 401

        if not validate_password(password):
            response_object = {
                "code":"401",
                "message":"password must need to math the requirment.",
                "data": {'paramater':"password"} 
            }
            return response_object, 401



        return f(*args, **kwargs)

    return decorated


def admin_token_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = request.headers.get('Authorization') 
        if not auth_token:
            response_object = {
                "code":"403",
                "message":"Authorization missed.",
                "data": {'Authorization':"fail"} 
            }
            return response_object, 403
        
        data, status = AuthService.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated
