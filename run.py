# Entry point for the application.
"""App entry point."""
import os, unittest
from flask import Flask, render_template
from flask_restx import Api, Namespace
from flask import Blueprint
from flask_migrate import Migrate
from flask_script import Manager
from dotenv import load_dotenv

# load .env into Flask application, including MySQL connection, jwt screct key, and password salt.
load_dotenv(override=True)

# import global variables
from app import create_app, db
from app.config import key

# Create api & swagger
app = create_app( config_name = os.getenv('PROD_ENV') or 'development')

blueprint = Blueprint('api', __name__, url_prefix="/api/v1")

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


app.app_context().push()

# create manager based on app application object
manager = Manager(app)
migrate = Migrate(app, db)
#manager.add_command('db', MigrateCommand)

# register the api_v1
api_v1 = Api(
    blueprint,
    title='Grapevine Leaf Disease Classification API Documents',
    version='1.0',
    description='a Grapevine Leaf Disease Classification for flask restplus (restx) web service',
    authorizations=authorizations,
    security='apikey', 
    # All API metadatas
)



# if using bluepoint as endpoint, we don't need to invoke init_app
#api_v1.init_app(app)

# import restful api 
from app.controllers.UserController import user_api as user_ns
from app.controllers.AuthController import user_auth_api as user_auth_ns
from app.controllers.PredictController import predict_api as predict_ns
from app.controllers.FeedbackController import feedback_api as feedback_ns

# if publishing a new restful api, adding namespace code here  is for publish service
api_v1.add_namespace(user_ns, path='/user')
api_v1.add_namespace(user_auth_ns, path='/auth')
api_v1.add_namespace(predict_ns, path='/predict')
api_v1.add_namespace(feedback_ns, path='/feedback')



#register bluepint as main endpoint of backend application
app.register_blueprint(blueprint)

# import user v2 restful api, it just test all function meet restapi standand. 
# register the api_v2
#blueprint_v2 = Blueprint('api_v2', __name__, url_prefix="/api/v2")
#api_v2 = Api(
#    blueprint_v2,
#    title='Grapevine Leaf Disease Classification API Documents',
#    version='2.0',
#    description='a Grapevine Leaf Disease Classification for flask restplus (restx) web service',
#    authorizations=authorizations,
#    security='apikey', 
#    # All API metadatas
#)


#from app.controllers.UserV2Controller import user_api_v2 as user_v2_ns
#api_v2.add_namespace(user_v2_ns, path='/user')

#register bluepint as endpoint of v2 in our backend application
#app.register_blueprint(blueprint_v2)


@app.route('/') 
@app.route('/index') 
def index():
    app.logger.info('%s successfully invoke /', "/")
    return render_template('index.html')



@app.route('/service/state')
def service_state():
    app.logger.info('successfully ', "/service/state")
    return {
        "code":"200",
        "message":"backend application runs",
        "data": {
            "enable": True
        }
    }

@manager.command
def run():
    app.run(host="0.0.0.0", debug=True, port=8080,ssl_context='adhoc')

@manager.command
def test():
    """Runs the unit tests."""

    tests = unittest.TestLoader().discover("app/test", pattern="test_auth.py")
    result = unittest.TextTestRunner(verbosity=3).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def test_predict():
    """Runs the unit tests."""

    tests = unittest.TestLoader().discover("app/test", pattern="test_predict.py")
    result = unittest.TextTestRunner(verbosity=3).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def test_user():
    """Runs the unit tests."""

    tests = unittest.TestLoader().discover("app/test", pattern="test_user.py")
    result = unittest.TextTestRunner(verbosity=3).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()