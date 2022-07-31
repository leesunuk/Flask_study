from pydoc import resolve
import unittest
from os import path
from urllib import response

from flask_login import current_user
from bs4 import BeautifulSoup

from blog import create_app
from blog import db
import os

from blog.models import User, get_user_model

basedir = os.path.abspath(os.path.dirname(__file__))
app = create_app()
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
        db.session.close()
        
        
    def tearDown(self):
        os.unlink('tests/test.db')
        self.ctx.pop()
    
    def test_signup_by_datebase(self):
   
        self.user_test_1 = get_user_model()(
            email = "ExEmail@test.com",
            username = "testname",
            password="test1234",
            is_staff=True
        )
        db.session.add(self.user_test_1)
        db.session.commit()
        
        self.user_test_2 =get_user_model()(
            email = "ExEx@test.com",
            username = "test2",
            password = "test1234"
        )
        db.session.add(self.user_test_2)
        db.session.commit()
        
        self.assertEqual(get_user_model().query.count(), 2)
        
        db.session.close()
        
        

    def test_signup_by_form(self):
        response = self.client.post('/auth/sign-up', data=dict(email="EEmail@test.com", username="testsname",password1="test1234",password2="test1234"))
        print("===",response.status_code,"===")
        self.assertEqual(get_user_model().query.count(), 1)
        db.session.close()
        db.engine.dispose()
    
    def test_before_login(self):
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        navbar_befor_login = soup.nav
        
        self.assertIn("Login", navbar_befor_login.text)
        self.assertIn("Sign Up", navbar_befor_login.text,)
        self.assertNotIn("Logout", navbar_befor_login.text,)
        response = self.client.post('/auth/sign-up',
                                    data=dict(email="exEmail@naver.com", username="test1", password1="test1234", password2="test1234"))
        with self.client:
            response = self.client.post('/auth/login',
                                        data=dict(email="exEmail@naver.com", username="test1", password="test1234"),
                                                  follow_redirects=True)
            soup = BeautifulSoup(response.data, 'html.parser')
            navbar_after_login = soup.nav
            
            self.assertIn(current_user.username, navbar_after_login.text)
            self.assertIn("Logout", navbar_after_login.text)
        
            self.assertNotIn("Login", navbar_after_login.text)
            self.assertNotIn("Sign up", navbar_after_login.text)
        db.session.close()