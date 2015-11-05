#!/usr/bin/python
# Libraries
import ConfigParser
import os

# Self imports
import handlers.imgur_handlers as imgur_handlers
from models.user import User as Imgur_User
import viewers.imgur_viewer as imgur_viewer

def get_credentials(elem):
    '''
    Helper function to grab credentials
    client_id and client_secret from a file
    hidden to others (auth.ini)
    '''
    config = ConfigParser.ConfigParser()
    # Relative path for credentials
    fn = os.path.join(os.path.dirname(__file__), 'auth.ini')
    config.read(fn)
    return config.get('credentials', str(elem))

def get_client_id():
    return get_credentials('client_id')

def get_client_secret():
    return get_credentials('client_secret')

def user_auth(cur_user):
    # Get necessary information about this application
    client_id = get_client_id()
    client_secret = get_client_secret()

    # Request Imgur account pin from user
    user_pin = imgur_viewer.request_pin(client_id)
    # Try to exchange pin for tokens
    user_tokens = imgur_handlers.get_user_token(client_id,
            client_secret, user_pin)
    
    if(user_tokens is not None):
        # TODO: Update cur_user
        
        cur_user.update_user(user_tokens)

        return True # Authorization succeeded

    return False # Authorization failed, return false

def basic_img_upload(img_url):
    cur_user = Imgur_User(get_client_id())

    print("Non-user image upload...")
    return imgur_handlers.upload_image(cur_user.get_header(), img_url)


# If you want to run as main, so be it! Here are some tests
if(__name__ == "__main__"):
    # Set up user
    cur_user = Imgur_User(get_client_id())
    
    # Test image upload without logged in user
    print("Testing image upload...")
    img_url = imgur_viewer.request_image_url()
    imgur_handlers.upload_image(cur_user.get_header(), img_url)
    
    # Log in user
    print("Testing Login...")
    user_auth(cur_user)

    # Test image upload with or without log in
    print("Testing image upload again...")
    img_url = imgur_viewer.request_image_url()
    imgur_handlers.upload_image(cur_user.get_header(), img_url)
    
