from pydoc import resolve
import unittest
from os import path
from urllib import response

from flask_login import current_user
from bs4 import BeautifulSoup

from blog import create_app
from blog import db
import os

from blog.models import User, get_user_model, get_post_model, get_category_model

basedir = os.path.abspath(os.path.dirname(__file__))
app = create_app()
app.testing = True

# class TestAuth(unittest.TestCase):
    
#     def setUp(self):
#         self.ctx = app.app_context()
#         self.ctx.push()
#         self.client = app.test_client()
        
#         self.db_uri = 'sqlite:///'+os.path.join(basedir, 'test.db')
#         app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#         app.config["SQLALCHEMY_DATABASE_URI"] = self.db_uri
#         if not path.exists("tests/" + "test_db"):
#             db.create_all(app=app)
#         db.session.close()
        
        
#     def tearDown(self):
#         os.unlink('tests/test.db')
#         self.ctx.pop()
    
    
    # def test_signup_by_datebase(self):
   
    #     self.user_test_1 = get_user_model()(
    #         email = "ExEmail@test.com",
    #         username = "testname",
    #         password="test1234",
    #         is_staff=True
    #     )
    #     db.session.add(self.user_test_1)
    #     db.session.commit()
        
    #     self.user_test_2 =get_user_model()(
    #         email = "ExEx@test.com",
    #         username = "test2",
    #         password = "test1234"
    #     )
    #     db.session.add(self.user_test_2)
    #     db.session.commit()
        
    #     self.assertEqual(get_user_model().query.count(), 2)
        
    #     db.session.close()
        
        

    # def test_signup_by_form(self):
    #     response = self.client.post('/auth/sign-up', data=dict(email="EEmail@test.com", username="testsname",password1="test1234",password2="test1234"))
    #     print("===",response.status_code,"===")
    #     self.assertEqual(get_user_model().query.count(), 1)
    #     db.session.close()
    #     db.engine.dispose()
    
    # def test_before_login(self):
    #     response = self.client.get('/')
    #     soup = BeautifulSoup(response.data, 'html.parser')
    #     navbar_befor_login = soup.nav
        
    #     self.assertIn("Login", navbar_befor_login.text)
    #     self.assertIn("Sign Up", navbar_befor_login.text,)
    #     self.assertNotIn("Logout", navbar_befor_login.text,)
    #     response = self.client.post('/auth/sign-up',
    #                                 data=dict(email="exEmail@naver.com", username="test1", password1="test1234", password2="test1234"))
    #     with self.client:
    #         response = self.client.post('/auth/login',
    #                                     data=dict(email="exEmail@naver.com", username="test1", password="test1234"),
    #                                               follow_redirects=True)
    #         soup = BeautifulSoup(response.data, 'html.parser')
    #         navbar_after_login = soup.nav
            
    #         self.assertIn(current_user.username, navbar_after_login.text)
    #         self.assertIn("Logout", navbar_after_login.text)
        
    #         self.assertNotIn("Login", navbar_after_login.text)
    #         self.assertNotIn("Sign up", navbar_after_login.text)
    #     db.session.close()
    
class TestPostwithCategory(unittest.TestCase):
    
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
        db.session.close()
        
    def test_add_category_and_post(self):
        self.python_category = get_category_model()(
            name="python"
        )
        db.session.add(self.python_category)
        db.session.commit()
        self.assertEqual(get_category_model().query.first().name, "python")
        self.assertEqual(get_category_model().query.first().id, 1)
        
        self.rust_category = get_category_model()(
            name="rust"
        )
        db.session.add(self.rust_category)
        db.session.commit()
        self.assertEqual(get_category_model().query.filter_by(id=2).first().name, "rust")
        
        self.javascript_category = get_category_model()(
            name = "javascript"
        )
        db.session.add(self.javascript_category)
        db.session.commit()
        
        response = self.client.get('/categories-list')
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIn('python', soup.text)
        self.assertIn('rust', soup.text)
        self.assertIn('javascript', soup.text)
        
        response = self.client.get('/create-post', follow_redirects=False)
        self.assertEqual(302, response.status_code)
        
        response = self.client.post('/auth/sign-up',
                                    data=dict(email="exEmail@test.com", username="test", password1="test1234", password2="test1234"))
        with self.client:
            response = self.client.post('/auth/login',
                                    data=dict(email="exEmail@test.com", username="test", password="test1234"), follow_redirects=True)
            response= self.client.get('/create-post')
            self.assertEqual(response.status_code, 200)
            
            soup = BeautifulSoup(response.data, 'html.parser')
            select_tags = soup.find(id='category')
            self.assertIn("python", select_tags.text)
            self.assertIn("rust", select_tags.text)
            self.assertIn("javascript", select_tags.text)
            
            response_post = self.client.post('/create-post',
                                             data=dict(title="안녕",
                                                       content="반가워",
                                                       category="1"),
                                             follow_redirects=True)
            self.assertEqual(1,get_post_model().query.count())
            
            response = self.client.get(f'/posts/1')
            soup = BeautifulSoup(response.data, 'html.parser')
            
            title_wrapper = soup.find(id='title-wrapper')
            self.assertIn("안녕", title_wrapper.text)
            
            author_wrapper = soup.find(id='author-wrapper')
            self.assertIn("hi", author_wrapper.text)
        db.session.close()
if __name__ == "__main__":
    unittest.main()
    db.session.close()
    
    def test_update_post(self):
        
        self.smith = get_user_model()(
            email = "smith@test.com",
            username = "smith",
            password = "1234",
            is_staff = True,
        )
        db.session.add(self.smith)
        db.session.commit()
        
        self.james = get_user_model()(
            email = "james@test.com",
            username = "james",
            password = "1234",
            is_staff = True,
        )
        db.session.add(self.james)
        db.session.commit()
        
        self.python_category = get_category_model()(
            name = "python"
        )
        db.session.add(self.python_category)
        db.session.commit()
        self.javascript_category = get_category_model()(
            name = "javascript"
        )
        db.session.add(self.javascript_category)
        db.session.commit()
        
        from flask_login import FlaskLoginClient
        app.test_cilent_class = FlaskLoginClient
        
        with app.test_client(user=self.smith) as smith:
            smith.post('/create-post',
                       data=dict(title="안녕, 나는 smith",
                                 content = "만나서 반가워!",
                                 category="1"), fllow_redirects=True)
            response = smith.get('/posts/1')
            soup = BeautifulSoup(response.data, 'html.parser')
            edit_button = soup.find(id='edit-button')
            self.assertIn('Edit', edit_button.text)
            
            response = smith.get('/edit-post/1')
            self.assertEqual(200, response.status_code)
            soup = BeautifulSoup(response.data, 'html.parser')
            
            title_input = soup.find('input')
            content_input = soup.find('textarea')
            
            self.assertIn(title_input.text, "안녕! smith야")
            self.assertIn(content_input.text, "만나서 반가워")
            
            smith.post('/edit-post/1',
                       data=dict(title="안녕! smith가 수정해볼게",
                                 content="수정이 잘 됐으면 좋겠어요",
                                 category="2"), follow_redirects=True)
            
            response = smith.get('/posts/1')
            soup = BeautifulSoup(response.data, 'html.parser')
            title_wrapper = soup.find(id='title-wrapper')
            content_wrapper = soup.find(id='content-wrapper')
            
            self.assertIn(title_input.text, "안녕 smith 글 수정할게")
            self.assertIn(content_input.text, "수정이 잘 됐으면 좋겠어요")
            
            response = smith.get('/posts/1')
            soup = BeautifulSoup(response.data, 'html.parser')
            edit_button = soup.find(id='edit-button')
            self.assertIn('Edit', edit_button.text)
            smith.get('/auth/logout')
            
        with app.test_client(user=self.james) as james:
            response = james.get('/posts/1')
            self.asserEqual(response.status_code, 200)
            soup = BeautifulSoup(response.data, 'html.parser')
            self.assertNotIn('Edit', soup.text)
            response = james.get('/edit-post/1')
            self.assertEqual(response.status_code, 403)