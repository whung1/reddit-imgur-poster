"""Imgur API-Handling methods ranging from requesting 
user authorization and tokens to image uploading"""

import requests

import json_handler as j_handler

def get_user_tokens_via_refresh(client_id, 
        client_secret, refresh_token):
    """Given the client_id, client_secret, and refresh token,
    get a new access token from the api and return it"""
    # Setup params
    params = {'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'grant_type': refresh_token}
    url = "https://api.imgur.com/oauth2/token"

    # POST to server using requests
    r = requests.post(url, data=params)

    # Get JSON response and parse
    j = r.json()
    return j_handler.parse_user_token_json(j)

def get_user_tokens_via_pin(client_id, client_secret, pin):
    """Given the client_id, client_secret,
    and pin from the user, exchange it for the 
    user's access and refresh tokens in a tuple where

    tuple[0] = access token
    tuple[1] = refresh token"""
    # Setup params and url to pass in
    params = {'client_id': client_id,
            'client_secret': client_secret,
            'pin': pin,
            'grant_type': 'pin'}
    url = 'https://api.imgur.com/oauth2/token'
        
    # POST to server using the requests library
    r = requests.post(url, data=params)

    # Get JSON response and parse
    j = r.json()
    return j_handler.parse_user_token_json(j)

def upload_image(header, image_url):
    """Uploads an image given a formed 
    authorization header and source image url
    
    returns dict of {success: True or False, 
                    'imgur_url': str (if success)
                    'error': str (if failure)}"""
    # Set up necessary elements to send to API
    upload_url = "https://api.imgur.com/3/upload"
    payload = {"image": image_url,
            "type": "URL"}

    # POST to server using the requests library
    r = requests.post(upload_url, data=payload, headers = header)

    # Get JSON response and parse
    j = r.json()
    return j_handler.parse_upload_image_json(j)
