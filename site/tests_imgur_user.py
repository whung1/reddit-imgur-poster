"""Test cases for the website Imgur_User model
and methods. Is tightly tied to the User model, and
assumes certain things (like an one-to-one way
relationship between User and Imgur_User models)"""

import unittest
import os

from flask import current_app, url_for
from flask.ext.testing import TestCase
from flask.ext.login import current_user

from app import app, bcrypt, db, login_manager
from app.models import User, Imgur_User

class ImgurUserTestCase(TestCase):

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

    def create_user(self, username="foo", email="foo@foo.com", pwd="password"):
        """Helper function to create a User entry
        in database through SQLAlchemy"""
        with app.app_context():
            user = User(username=username,
                        email=email,
                        pwd=bcrypt.generate_password_hash(pwd))
            db.session.add(user)
            db.session.commit()

    def login_user(self, username="foo", pwd="password"):
        """Helper function to log a user in using the
        site's login function"""
        return self.client.post(url_for('login'),
                                data = {'username': username,
                                'password': pwd})

    def create_imgur_user(self,
            imgur_username="imgur_foo",
            access_token="notrealaccesstoken",
            refresh_token="notrealrefreshtoken"):
        """Helper function grabs the first User in the database
        and then binds a Imgur_User to it"""
        with app.app_context():
            cur_user = User.query.first()
            if(cur_user is None):
                print("Error, need to create a User first")
                self.assertFalse(True)
            imgur_usr = Imgur_User(username=imgur_username,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    user_id = cur_user.id)
            db.session.add(imgur_usr)
            db.session.commit()

    # Test 1
    def test_imgur_user_as_string(self):
        """Is the representation of the 
        User model what we expect?"""
        with app.app_context():
            self.create_user()
            self.create_imgur_user()
            imgur_usr = Imgur_User.query.first()
            representation = '<Imgur_User %r>' % unicode("imgur_foo")
            self.assertTrue(str(imgur_usr) == representation)
            return True

    # Test 2
    def test_imgur_user_model_structure(self):
        """Is the model representation relationship what we expect?"""
        with app.app_context():
            self.create_user()
            self.create_imgur_user()
            user = User.query.first()
            imgur_user = Imgur_User.query.first()
            self.assertTrue(user.id == imgur_user.user_id)
            return True

    # Test 3
    def test_imgur_user_flask_current_user(self):
        """Can we properly make a link to the
        current_user as given by flask login?"""
        with app.app_context():
            with self.client:
                self.create_user()
                self.create_imgur_user()
                self.login_user()
                imgur_user = Imgur_User.query.first()
                self.assertTrue(current_user.id == imgur_user.user_id)

    # Test 4
    def test_user_delete_imgur_child(self):
        """After using delete, does the child Imgur_User
        of a User get properly deleted from the site?"""
        with app.app_context():
            with self.client:
                self.create_user()
                self.login_user()
                # link a imgur child model to test
                imgur_usr = Imgur_User(username="imgur_child",
                        refresh_token="notactuallyatoken",
                        user_id=current_user.id)
                db.session.add(imgur_usr)
                db.session.commit()
                # Make sure the imgur child exists
                imgur_usr = Imgur_User.query.first()
                self.assertFalse(imgur_usr is None)
                self.assertTrue(imgur_usr.user_id == current_user.id)
                # user delete
                response = self.client.post(url_for("account_delete"),
                        data = {'password': "password"})
                user = User.query.first()
                self.assertTrue(user is None)
                imgur_usr = Imgur_User.query.first()
                self.assertTrue(imgur_usr is None)
                return True

if __name__ == '__main__':
    unittest.main()
