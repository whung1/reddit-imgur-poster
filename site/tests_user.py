"""Test cases for the website User model
and methods pertaining to it, especially those
reliant on Flask-Login"""
import unittest
import os

from flask import current_app, url_for
from flask.ext.testing import TestCase
from flask.ext.login import current_user

from app import app, db, bcrypt, login_manager
from app.models import User, Reddit_User

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
        """Testing helper function to create
        a user in database manually"""
        with app.app_context():
            user = User(username=username,
                        email=email,
                        pwd=bcrypt.generate_password_hash(pwd))
            db.session.add(user)
            db.session.commit()

    def login_helper(self, username="foo", pwd="password"):
        """Helper function to log a user in using the
        site's login function"""
        return self.client.post(url_for('login'),
                                data = {'username': username,
                                'password': pwd})

    # Test 1
    def test_user_as_string(self):
        """Is the representation of the 
        User model what we expect?"""
        with app.app_context():
            self.user_create_helper()
            user = User.query.first()
            representation = '<User %r>' % unicode('foo')
            self.assertTrue(str(user) == representation)
            return True

    # Test 2
    def test_get_user(self):
        """Can we retrieve the User instance created in setUp?"""
        with app.app_context():
            self.user_create_helper()
            user = User.query.first()
            self.assertTrue(bcrypt.check_password_hash(user.pwd,
                                                'password'))
            return True

    # Test 3
    def test_user_login(self):
        """Does the login method for the 
        User model work as expected?"""
        with app.app_context():
            with self.client:
                self.user_create_helper()
                response = self.login_helper()
                self.assert_redirects(response, url_for('home'))
                self.assertTrue(current_user)
                self.assertTrue(current_user.is_active)
                self.assertTrue(current_user.username == 'foo')
                self.assertTrue(current_user.is_authenticated())
                return True

    # Test 4
    def test_user_login_nonuser(self):
        """Does the login method refuse
        to login a user that doesn't exist?"""
        with app.app_context():
            with self.client:
                response = self.login_helper('fakeuser','fakepwd')
                self.assertFalse(current_user.is_active)
                self.assert_redirects(response, url_for('login'))
                return True

    # Test 5
    def test_user_registration(self):
        """Does the register method for
        the User model work as expected?"""
        with app.app_context():
            with self.client:
                self.client.post(url_for("register_process"),
                        data = {"username": "foo",
                            "email": "foo@foo.com",
                            "password": "password",
                            "confirm-password": "password"})
                user = User.query.first()
                self.assertFalse(user is None)
                self.assertTrue(user.username == "foo")
                self.assertTrue(user.email == "foo@foo.com")
                self.assertTrue(bcrypt.check_password_hash(user.pwd, 
                    "password"))
                return True

    # Test 6
    def test_user_registration_passwords_nonmatch_fail(self):
        """Does the register method reject
        properly when passwords do not match?"""
        with app.app_context():
            with self.client:
                self.client.post(url_for("register_process"),
                        data = {"username": "foo",
                            "email": "foo@foo.com",
                            "password": "password",
                            "confirm-password": "notsame"})
                user = User.query.first()
                self.assertTrue(user is None)
                return True

    # Test 7
    def test_user_logon_fail_nonuser(self):
        """Does the login method refuse
        to login a user that doesn't exist?"""
        with app.app_context():
            with self.client:
                response = self.login_helper('fakeuser','fakepwd')
                self.assertFalse(current_user.is_active)
                self.assert_redirects(response, url_for('login'))
                return True

    # Test 8
    def test_user_logout(self):
         """Does the logout method work
         for exisiting User model?"""
         with app.app_context():
             with self.client:
                 self.user_create_helper()
                 response = self.login_helper()
                 self.assertTrue(current_user.is_active)
                 response = self.client.get(url_for('logout'))
                 self.assert_redirects(response, url_for('login'))
                 self.assertFalse(current_user.is_active)
                 return True

    # Test 9
    def test_user_delete(self):
        """Can a user be deleted from
        the site through the delete function?"""
        with app.app_context():
            with self.client:
                self.user_create_helper()
                self.login_helper()
                # user delete
                response = self.client.post(url_for("account_delete"),
                        data = {'password': "password"})
                self.assert_redirects(response, url_for("login"))
                user = User.query.first()
                self.assertTrue(user is None)
                return True
    
    # Test 10
    def test_user_delete_children(self):
        """After using delete, does the children 
        of a User get properly deleted from the site?"""
        with app.app_context():
            with self.client:
                self.user_create_helper()
                self.login_helper()
                # link a reddit child model to test
                reddit_usr = Reddit_User(username="reddit_child",
                        refresh_token="notactuallyatoken",
                        user_id=current_user.id)
                db.session.add(reddit_usr)
                db.session.commit()
                # Make sure the reddit child exists
                reddit_usr = Reddit_User.query.first()
                self.assertFalse(reddit_usr is None)
                self.assertTrue(reddit_usr.user_id == current_user.id)
                # user delete
                response = self.client.post(url_for("account_delete"),
                        data = {'password': "password"})
                user = User.query.first()
                self.assertTrue(user is None)
                reddit_usr = Reddit_User.query.first()
                self.assertTrue(reddit_usr is None)
                return True
    
    # Test 11
    def test_user_delete_wrong_password(self):
        """Will a user be deleted from the
        site without the correct password?"""
        with app.app_context():
            with self.client:
                self.user_create_helper()
                self.login_helper()
                # user delete attempt
                response = self.client.post(url_for("account_delete"),
                        data = {'password': "12938129dasdmkmsd"})
                self.assert_redirects(response, url_for("account"))
                user = User.query.first()
                self.assertFalse(user is None)
                return True

    # Test 12
    def test_user_delete_wrong_form(self):
        """Will a user be deleted from simple
        incorrect POSTing?"""
        with app.app_context():
            with self.client:
                self.user_create_helper()
                self.login_helper()
                # user delete
                response = self.client.post(url_for("account_delete"),
                        data = {'notvidd': "whatever"})
                self.assert_redirects(response, url_for("account"))
                user = User.query.first()
                self.assertFalse(user is None)
                return True

if __name__ == '__main__':
    unittest.main()
