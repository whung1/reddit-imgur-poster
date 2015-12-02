"""Basic tests for the Reddit Imgur Upload site application."""
import unittest
import os

from flask import current_app, url_for
from flask.ext.testing import TestCase
from flask.ext.login import current_user

from app import app, bcrypt, login_manager
import app.imgur_backend.imgur_controller as im_control

class BasicTestCase(TestCase):
    """Basic test cases for the site app
    Includes test cases for basic image uploading
    and @login_required checks for Flask-Login"""

    def create_app(self):
        app.testing = True
        app.config['SITE_NAME'] = 'www.foo.com'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['HASH_ROUNDS'] = 1
        app.config['FILE_DIRECTORY'] = os.path.abspath(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'files'))
        with app.app_context():
            bcrypt.init_app(current_app)
            login_manager.login_view = "login"
            self.app = app.test_client()
        return app

    def setUp(self):
        return
    
    def tearDown(self):
        return
    
    # Test 1
    def test_valid_basic_image_upload(self):
        """Given a VALID img url, can we
        do a basic upload of the image?"""
        img_url = "http://placehold.it/120x120&text=image1"
        imgur_usr = None
        response = im_control.image_upload(imgur_usr, img_url)
        assert response['success'] == True

    # Test 2
    def test_invalid_basic_image_upload(self):
        """Given an INVALID img url, will
        we get failure message"""
        img_url = "http://blsjdfkj.com/aslkda.png"
        imgur_usr = None
        response = im_control.image_upload(imgur_usr, img_url)
        assert response['success'] == False

    def no_login_redirect_get_helper(self, get_url):
        """ Helper function to test redirects
        for when there is no user logged in"""
        with app.app_context():
            with self.client:
                self.assertFalse(current_user.is_active)
                response = self.client.get(url_for(get_url),
                                           follow_redirects=True)
 
    def no_login_redirect_post_helper(self, post_url):
        """ Helper function to test post redirects
        for when there is no user logged in"""
        with app.app_context():
            with self.client:
                self.assertFalse(current_user.is_active)
                response = self.client.post(url_for(post_url),
                                            follow_redirects=True)

    # Test 3
    def test_no_login_redirect_logout(self):
        """Does the logout method redirect
        properly if no user is logged in"""
        self.no_login_redirect_get_helper('logout')

    # Test 4
    def test_no_login_redirect_home(self):
        """Does the home method redirect
        properly if no user is logged in"""
        self.no_login_redirect_get_helper('home')

    # Test 5
    def test_no_login_redirect_account(self):
        """Does the account method redirect
        properly if no user is logged in"""
        self.no_login_redirect_get_helper('account')

    # Test 6
    def test_no_login_redirect_account_imgur(self):
        """Does the account_imgur method redirect
        properly if no user is logged in"""
        self.no_login_redirect_get_helper('account_imgur')

    # Test 7
    def test_no_login_redirect_account_reddit(self):
        """Does the account_reddit method redirect
        properly if no user is logged in"""
        self.no_login_redirect_get_helper('account_reddit')
    # Test 8
    def test_no_login_redirect_account_imgur_link(self):
        """Does the account_imgur_link method redirect
        properly if no user is logged in"""
        self.no_login_redirect_post_helper('account_imgur_link')

    # Test 9
    def test_no_login_redirect_account_imgur_unlink(self):
        """Does the account_imgur_unlink method redirect
        properly if no user is logged in"""
        self.no_login_redirect_post_helper('account_imgur_unlink')

    # Test 10
    def test_no_login_redirect_account_reddit_link(self):
        """Does the account_reddit_link method redirect
        properly if no user is logged in"""
        self.no_login_redirect_post_helper('account_reddit_link')

    # Test 11
    def test_no_login_redirect_account_reddit_unlink(self):
        """Does the account_reddit_unlink method redirect
        properly if no user is logged in"""
        self.no_login_redirect_post_helper('account_reddit_unlink')
    
    # Test 12
    def test_no_login_redirect_upload_and_post(self):
        """Does the upload_and_post method redirect
        properly if no user is logged in"""
        self.no_login_redirect_post_helper('upload_and_post')

    # Test 13
    def test_no_login_redirect_account_delete(self):
        """Does the upload_and_post method redirect
        properly if no user is logged in"""
        self.no_login_redirect_post_helper('account_delete')

if __name__ == '__main__':
    unittest.main()
