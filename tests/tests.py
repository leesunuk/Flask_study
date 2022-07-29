import unittest
from os import path

from flask_login import current_user
from bs4 import BeautifulSoup

from blog import create_app
from blog import db
import os

from blog.models import User

basedir = os.path.abspath(os.path.dirname(__file__))
app = create_app
app.testing = True

class TestAuth(unittest.TestCase):
    
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        
        self.db_uri = 'sqlite:///'+os.path.join(basedir, 'test.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = self.db_uri
        if not path.exists("tests/" + "test_db"):
            db.create_all(app=app)
        
    def tearDown(self):
        os.remove('test.db')
        self.ctx.pop()
        
    
    def test_signup_by_datebase(self):
        self.user_test_1 = User(
            email = "ExEmail@test.com",
            username = "testname",
            password="test1234",
            is_staff=True
        )
        db.session.add(self.user_test_1)
        db.session.commit()
        
        self.user_test_2 = User(
            email = "ExEx@test.com",
            username = "test2",
            password = "test1234"
        )
        db.session.add(self.user_test_2)
        db.session.commit()
        
        self.assertEqual(User.query.count(), 2)
    
    def test_signup_by_form(self):
        response = self.client.post('/auth/sign-up', data=dict(email="e"))
        