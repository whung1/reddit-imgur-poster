#!/usr/bin/python
# Libraries
import ConfigParser
import os

# Self imports
import handlers.imgur_handlers as imgur_handlers
import models.user as imgur_user_handlers
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

def get_request_pin_url():
    # Generate the url for pin request
    client_id = get_client_id()
    req_resp = "pin"
    state = "anything"
    url = 'https://api.imgur.com/oauth2/authorize?client_id={cid}&response_type={resp}&state={app_state}'
    url = url.format(cid=client_id, resp= req_resp, app_state = state)
    return url

def exchange_pin_for_tokens(user_pin):
    # Get necessary information about this application
    client_id = get_client_id()
    client_secret = get_client_secret()

    # Try to exchange pin for tokens
    return imgur_handlers.get_user_tokens(client_id,
            client_secret, user_pin)

def user_auth(user_pin, cur_user):
    user_tokens = exchange_pin_for_tokens(user_pin)

    if(user_tokens is not None):
        # TODO: Update cur_user
        
        cur_user.update_user(user_tokens)

        return True # Authorization succeeded

    return False # Authorization failed, return false

def image_upload(imgur_user, img_url):
    cur_header = get_header(imgur_user)
    return imgur_handlers.upload_image(cur_header, img_url)

def get_header(imgur_user):
    return imgur_user_handlers.get_header(imgur_user, get_client_id())

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
    # Request Imgur account pin from user
    user_pin = imgur_viewer.request_pin(get_client_id())
    user_auth(user_pin, cur_user)

    # Test image upload with or without log in
    print("Testing image upload again...")
    img_url = imgur_viewer.request_image_url()
    imgur_handlers.upload_image(cur_user.get_header(), img_url)
    
