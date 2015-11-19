import os

from flask import current_app, url_for
from flask.ext.testing import TestCase
from flask.ext.login import current_user

from app import app, db, bcrypt, login_manager
from app.models import User

class UserTestCase(TestCase):

    def create_app(self):
        app.testing = True
        app.config['SITE_NAME'] = 'www.foo.com'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['HASH_ROUNDS'] = 1
        app.config['FILE_DIRECTORY'] = os.path.abspath(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'files'))
        with app.app_context():
            db.init_app(current_app)
            bcrypt.init_app(current_app)
            login_manager.login_view = "login"
            self.db = db
            self.app = app.test_client()
        return app

    def setUp(self):
        """Set up database"""
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Empty the database for next test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def user_create_helper(self, username="foo", email="foo@foo.com", pwd="password"):
        with app.app_context():
            user = User(username=username,
                        email=email,
                        pwd=bcrypt.generate_password_hash(pwd))
            db.session.add(user)
            db.session.commit()

    # Test 1
    def test_user_as_string(self):
        """Is the representation of the 
        User model what we expect?"""
        with app.app_context():
            self.user_create_helper()
            user = User.query.get(1)
            representation = '<User %r>' % unicode('foo')
            assert str(user) == representation

    # Test 2
    def test_get_user(self):
        """Can we retrieve the User instance created in setUp?"""
        with app.app_context():
            self.user_create_helper()
            user = User.query.filter_by(username="foo").first()
            assert bcrypt.check_password_hash(user.pwd,
                                                'password')
            return True

    def login_helper(self, username, pwd):
        return self.client.post(url_for('login'),
                                data = {'username': username,
                                'password': pwd})

    # Test 3
    def test_login_user(self):
        """Do the login methods for the 
        User model work as expected?"""
        with app.app_context():
            with self.client:
                self.user_create_helper()
                response = self.login_helper('foo', 'password')
                self.assert_redirects(response, url_for('home'))
                self.assertTrue(current_user)
                self.assertTrue(current_user.is_active)
                self.assertTrue(current_user.username == 'foo')
                self.assertTrue(current_user.is_authenticated())
                return True

    # Test 4
    def test_logout_user(self):
         """Does the logout method work
         for exisiting User model?"""
         with app.app_context():
             with self.client:
                 self.user_create_helper()
                 response = self.login_helper('foo', 'password')
                 self.assertTrue(current_user.is_active)
                 response = self.client.get(url_for('logout'))
                 self.assert_redirects(response, url_for('login'))
                 self.assertFalse(current_user.is_active)
                 return True

    # Test 5
    def test_login_non_user(self):
        """Does the login method refuse
        to login a user that doesn't exist?"""
        with app.app_context():
            with self.client:
                response = self.login_helper('fakeuser','fakepwd')
                self.assertFalse(current_user.is_active)
                self.assert_redirects(response, url_for('login'))
                return True

    # TODO: user delete
    # TODO: Register and delete test cases
