from flask_testing import TestCase
from app.config import config
from app import db
from run import app
#from flask import current_app as app

class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object(config['testing'])
        return app

    def setUp(self):
        #pass
        db.create_all()
        db.session.commit()

    def tearDown(self):
        #pass
        db.session.remove()
        db.drop_all()