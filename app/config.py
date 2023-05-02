import os
PASSWORD_SECRET_KEY = os.urandom(32)
JWT_SECRET_KEY =  os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    PASSWORD_SECRET_KEY = os.getenv('PASSWORD_SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRT_KEY')
    DEBUG = False
    # Swagger
    RESTX_MASK_SWAGGER = False

class DevelopmentConfig(Config):
    DEBUG = True
    # Swagger
    RESTX_MASK_SWAGGER = True

class TestingConfig(Config):
    DEBUG = True
    # Swagger
    RESTX_MASK_SWAGGER = True

class ProductConfig(Config):
    DEBUG = False
    # Swagger
    RESTX_MASK_SWAGGER = False


# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = False
# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
    'product': ProductConfig,
}

key = Config.PASSWORD_SECRET_KEY
jwt_key = Config.JWT_SECRET_KEY

