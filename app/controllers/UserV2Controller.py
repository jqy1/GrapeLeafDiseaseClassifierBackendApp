import sys,json
from flask import request
from flask_restx import Api, Resource, fields, Namespace
from werkzeug.middleware.proxy_fix import ProxyFix
#import current_app aka flask, as for logging
from flask import current_app as app

# import user model & dao
from ..utils.decorator import token_required, admin_token_required, register_valiation

# create user api namespace 
user_api_v2 = Namespace('users', description='User operations')



@user_api_v2.route('/')
class UserListV2Resource(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''

    @user_api_v2.doc('get all users from database')
    @token_required
    def get(self):
        '''
         A function that mobile application or web application can fetch all user profile.
        '''
        app.logger.info('%s successfully invoke UserController', "index")
        #app.logger.info(user_db)
        app.logger.info(users)
        return { 
            'code':200,
            'message':'todo:coming soon',
            'data': {}  
        }, 200