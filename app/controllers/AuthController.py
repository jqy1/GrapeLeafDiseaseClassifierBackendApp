from flask import request
from flask_restx import Api, Resource, fields, Namespace
from flask import current_app as app
from typing import Dict, Tuple

# import user model & dao
from ..models.User import User
from ..service.AuthService import AuthService

user_auth_api = Namespace('auth', description='authentication related operations')

user_auth = user_auth_api.model('auth_details', {
    'email': fields.String(required=True, description='The email address'),
    'password': fields.String(required=True, description='The user password '),
})


user_auth_token = user_auth_api.model('auth_token', {
    'Authorization': fields.String(required=True, description='the auth token that issue by server', ),
})


user_auth_token_logout_response = user_auth_api.model('auth_details_response', {
    'code': fields.Integer(readonly=True, description='a response code from backend application'),
    'message': fields.String(required=True, description='messages that send to client '),
    'data': fields.Nested(user_auth_token),
})


user_auth_token_logout_response_401 = user_auth_api.model('auth_details_response', {
    'code': fields.Integer(readonly=True, description='a response code from backend application'),
    'message': fields.String(required=True, description='messages that send to client '),
    'data': fields.Nested(user_auth_token),
})

user_auth_token_logout_response_403 = user_auth_api.model('auth_details_response', {
    'code': fields.Integer(readonly=True, description='a response code from backend application'),
    'message': fields.String(required=True, description='messages that send to client '),
})


user_auth_response = user_auth_api.model('auth_details_response', {
    'code': fields.Integer(readonly=True, description='a response code from backend application',),
    'message': fields.String(required=True, description='messages that send to client '),
    'data': fields.Nested(user_auth_token),
})

@user_auth_api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @user_auth_api.doc('user login') 
    @user_auth_api.marshal_with(user_auth_response, code=200)
    @user_auth_api.marshal_with(user_auth_token_logout_response_401, code=401)
    @user_auth_api.expect(user_auth, validate=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        """ 
            A login function of grapevine leaf systen, this function can invoke by any clients, then issue a Json web token (JWT) when authorized.
        """
        # get the post data
        post_data = request.json
        return AuthService.login_user(data=post_data)


@user_auth_api.route('/logout')
class UserLogoutAPI(Resource):
    """
    Logout Resource
    """
    @user_auth_api.doc('logout a user')
    @user_auth_api.marshal_with(user_auth_token_logout_response, code=200)
    @user_auth_api.marshal_with(user_auth_token_logout_response_401, code=401)
    @user_auth_api.marshal_with(user_auth_token_logout_response_403, code=403)
    def post(self) -> Tuple[Dict[str, str], int]:
        # logout a user
        """ 
            A logout function of grapevine leaf systen, this function can invoke by any clients based on restful api with JWT.
        """
        auth_header = request.headers.get('Authorization')
        return AuthService.logout_user(data=auth_header)