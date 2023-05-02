from flask import request
from flask_restx import Api, Resource, fields, Namespace
from flask import current_app as app
from typing import Dict, Tuple

# import user model & dao
from ..models.User import User
from ..service.UserService import UserService
from .AuthController import user_auth_token
from ..utils.decorator import token_required, admin_token_required, register_valiation

# create user api namespace 
user_api = Namespace('users', description='User operations')

user = user_api.model('User', {
    'first_name': fields.String(required=True, description='first_name'),
    'sur_name': fields.String(required=True, description='sur_name'),
    'mail': fields.String(required=True, description='mail'),
    'password_hash': fields.String(required=True, description='password_hash'),
    'user_name': fields.String(required=True, description='user_name'),
})

user_response = user_api.model('registration_response', {
    'code': fields.Integer(readonly=True, description='a response code from backend application',),
    'message': fields.String(required=True, description='messages that send to client '),
    'data': fields.Nested(user_auth_token),
})

user_response_201 = user_api.model('registration_response_201', {
    'code': fields.Integer(readonly=True, description='a response code from backend application',),
    'message': fields.String(required=True, description='messages that send to client '),
    'data': fields.Nested(user_auth_token),
})

user_response_401 = user_api.model('registration_response_401', {
    'code': fields.Integer(readonly=True, description='a response code from backend application',),
    'message': fields.String(required=True, description='messages that send to client '),
    'data': fields.Nested(user_auth_token),
})


@user_api.route('/<user_id>', endpoint='/')
@user_api.doc(params={'user_id': 'A User ID'})
class UserResource(Resource):
    @user_api.doc(responses={403: 'Not Authorized'})
    @token_required
    def get(self, user_id) -> Tuple[Dict[str, str], int]:
        '''
         A function that mobile application or web application can fetch all user profile by a user's union id (email).
        '''
        app.logger.info('%s successfully invoke UserController', "show")
        user = UserService.get(user_id)
        return {
            "code": "200" if user is not None else "201" ,
            "message":"succeed" if user is not None else "User is not exist!" ,
            "data": [ user if user is not None else "Empty" , ] 
        }

    @user_api.doc(responses={403: 'Not Authorized'})
    @token_required
    def put(self, user_id) -> Tuple[Dict[str, str], int]:
        '''
         A help function for mobile application or web application can modify their basic information, including first name, last name, and others.
        '''
        user_api.abort(403)
    

    @user_api.doc('delete a user account, it does not a physical delete, and only disable a user to login into the system ')
    @user_api.expect()
    @token_required
    def delete(self,user_id)-> Tuple[Dict[str, str], int]:
        '''
         A delete function that can remove themselves from mobile application or web application.
        '''
        app.logger.info('%s successfully invoke UserController', "delete")
        return {
            "code":"204",
            "message":"the delete method does not implement",
            "data": [] 
        }

@user_api.route('/')
class UserListResource(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''

    @user_api.doc('get all users from database')
    @token_required
    def get(self)-> Tuple[Dict[str, str], int]:
        '''
         A function that mobile application or web application can fetch all user profile.
        '''
        app.logger.info('%s successfully invoke UserController', "index")
        #app.logger.info(user_db)
        users = UserService.get_all()
        app.logger.info(users)
        return { 
            'code':200,
            'message':'succeed',
            'data': users  
        }, 200

    @user_api.expect(user, validate=True)
    @user_api.marshal_with(user_response,code=200,)
    @user_api.marshal_with(user_response_201,code=201, )
    @user_api.marshal_with(user_response_401,code=401, )
    @register_valiation
    def post(self) -> Tuple[Dict[str, str], int]:
        '''
         A registeraton function for mobile application or web application, it accepts a json object of user.
        '''

        data = request.json
        response_object, code  = UserService.create(data=data)

        return  response_object, code