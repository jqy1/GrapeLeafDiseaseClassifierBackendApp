import os
from flask import Flask, render_template,session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy
from .config import config,key,jwt_key

db = SQLAlchemy()

flask_bcrypt = Bcrypt()


def create_app( config_name : str ) -> Flask:
    # create and configure the app
    app = Flask(__name__)
    # Load config file based input 
    app.config.from_object(config[config_name])

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.secret_key = os.getenv("SECRET_KEY")
    
    app.flask_bcrypt = Bcrypt()

    db.init_app(app)

    flask_bcrypt.init_app(app)

    app.flask_bcrypt.init_app(app)

    #app.logger.debug(app.config)
    return app