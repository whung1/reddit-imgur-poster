#!/usr/bin/python
# Libraries
import ConfigParser
import os
from flask import flash

# Self imports
import handlers.api_handler as api_handler
import handlers.user_handler as user_handler
import viewers.imgur_viewer as imgur_viewer


def get_credentials(elem, filename='auth.ini'):
    """Helper function to grab credentials
    from an ini file hidden to others (auth.ini)"""

    config = ConfigParser.ConfigParser()
    # Relative path for credentials
    fn = os.path.join(os.path.dirname(__file__), filename)
    config.read(fn)
    return config.get('credentials', str(elem))

def get_client_id():
    return get_credentials('client_id')

def get_client_secret():
    return get_credentials('client_secret')

def get_request_pin_url():
    # Generate the url for pin request
    # TODO: Meaningful state
    client_id = get_client_id()
    req_resp = "pin"
    state = "anything"
    url = 'https://api.imgur.com/oauth2/authorize?client_id={cid}&response_type={resp}&state={app_state}'
    url = url.format(cid=client_id, resp= req_resp, app_state = state)
    return url

def refresh_access_token(db, imgur_user):
    """Refreshes the access token for a given
    imgur user if necessary
    
    Returns True if access token is valid (not expired), 
    Returns False otherwise"""
    # Check whether the access token for imgur_user is valid/expired
    if (user_handler.access_token_expired(imgur_user, 0)):
        # If expired, use refresh token for a new access token
        refresh_token = user_handler.get_refresh_token(imgur_user)
        response = api_handler.get_user_tokens_via_refresh(
                get_client_id(), get_client_secret(), refresh_token)

        if (response['success'] == True):
            user_handler.set_access_token(imgur_user, 
                    response['access_token'])
            user_handler.set_refresh_token(imgur_user,
                    response['refresh_token'])
            db.session.add(imgur_user)
            db.session.commit()
            flash("Your access token expired, so we went through the liberty to refresh it")
            return True
        elif (response['success'] == False):
            flash("Failed to refresh access token")
            return False
    else:
        # If not expired, simply return True
        return True

def exchange_pin_for_tokens(user_pin):
    # Get necessary information about this application
    client_id = get_client_id()
    client_secret = get_client_secret()
    # Try to exchange pin for tokens
    return api_handler.get_user_tokens_via_pin(client_id,
            client_secret, user_pin)

def user_auth(user_pin, cur_user):
    user_tokens = exchange_pin_for_tokens(user_pin)

    if(user_tokens is not None):
        # TODO: Update cur_user
        
        cur_user.update_user(user_tokens)

        return True # Authorization succeeded

    return False # Authorization failed, return false

def image_upload(db, img_url, imgur_user=None):
    """Upload an image to imgur either through
    the app or through the imgur user if the imgur
    user has necessary requirements (logged in)"""
    auth_header = get_header(db, imgur_user)
    return api_handler.upload_image(auth_header, img_url)

def get_header(db, imgur_user):
    """Helper method to grab the correct 
    authorization headers for user-specific api calls"""
    refresh_access_token(db, imgur_user)
    return user_handler.get_header(imgur_user, get_client_id())








# TODO: Make actual test cases
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
    
