import uuid,datetime
from flask import current_app as app
from flask import session,request
from flask_sqlalchemy import SQLAlchemy
from typing import Dict, Tuple
from ..models.User import User as User
from .. import db
from ..config import jwt_key, key

class AuthService(object):

    """
        AuthService class allows to login, logout operation
    """
    def __init__(self):
        pass

    @staticmethod
    def add_auth_token_session(token:str, email:str):
        """ using session stores the current login token for validation. """
        #app.logger.debug(f'add_auth_token_session -> ${token}')
        if email in session:
            previous_auth_token = session[email]
            session.pop(previous_auth_token)
            session.pop(email)

        session[token] = email
        session[email] = token
        #app.logger.debug(session)


    @staticmethod
    def remove_auth_token_session(token:str):
        if token in session:
            email = session[token]
            session.pop(token)
            session.pop(email)

        #app.logger.debug(f"remove_auth_token_session -> ${token}")
        #app.logger.debug(session)


    @staticmethod
    def login_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        try:
            email = data['email']
            user = User.query.filter_by(mail=email).first()
            if user:
                if user.check_password(data["password"]):
                    auth_token = User.encode_auth_token(user.id)
                    if auth_token:

                        AuthService.add_auth_token_session(auth_token, email)

                        response_object = {
                            "code":200,
                            "message":"Successfully logged in.",
                            "data": {'Authorization':auth_token} 
                        }
                        return response_object, 200
                    else:
                        response_object = {
                            "code":403,
                            "message":"token generating wrong",
                            "data": {'Authorization':"fail"} 
                        }
                else:
                    response_object = {
                        "code":402,
                        "message":"password wrong",
                        "data": {'Authorization':"fail"} 
                    }
                    return response_object,402
            else:
                response_object = {
                    "code":401,
                    "message":"user is not exist",
                    "data": {'Authorization':"fail"} 
                }
                return response_object,401

        except Exception as e:
            response_object = {
                "code":500,
                "message":"Try again.",
                "data": {'Authorization':"fail"} 
            }
            return response_object,500

    @staticmethod
    def logout_user(data: str) -> Tuple[Dict[str, str], int]:
        
        auth_token = request.headers.get('Authorization') 
        if auth_token:
            
            resp = User.decode_auth_token(auth_token)

            if not isinstance(resp, str):
                #remove token from current session
                AuthService.remove_auth_token_session(auth_token)
                # mark the token as blacklisted
                return AuthService.save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        #app.logger.debug('token -> %s', auth_token)
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            #app.logger.debug('resp -> %s', resp)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    'code': 200,
                    'message':'Successfully logged in.',
                    'data': {
                        'user_id': user.id,
                        'email': user.mail,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401

    @staticmethod
    def save_token(token: str) -> Tuple[Dict[str, str], int]:
        response_object = {
            'code': 200,
            'message':'Successfully logout.',
            'data': {
                'Authorization': "None",
            }
        }
        return response_object, 200