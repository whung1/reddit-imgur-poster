#!/usr/bin/python
import base64
import json
import requests
import pprint

from base64 import b64encode
import json_handlers as j_handlers

'Imgur Handler Functions Class'

# TODO: Implement non-pin login
def login(username, pwd):
    print('Username: ' + username + ', password: '  + pwd)
    
def get_user_token(client_id, client_secret, pin):
    ''' Given the client_id, client_secret, and pin from the user, exchange it for
    the user's access and refresh tokens in a tuple where

    tuple[0] = access token
    tuple[1] = refresh token
    '''
    # Setup params and url to pass in
    params = {'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'pin',
            'pin': pin}
    url = 'https://api.imgur.com/oauth2/token'
        
    # POST to server using the requests library
    r = requests.post(url, data=params) #verify=False is for SSL, for some reason throws error? Check later
    # Get JSON response and parse
    j = r.json()
    return j_handlers.parse_user_token_json(j)


def upload_image(header, image_url):
    """ Uploads an image given a
    formed header and source image url
    
    TODO: returns dict of {success: True or False, imgur_link: str}
    """
    # Set up necessary elements to send to API
    upload_url = "https://api.imgur.com/3/upload"
    payload = {"image": image_url,
            "type": "URL"
            }

    r = requests.post(upload_url, data=payload, headers = header)

    j = r.json()
    new_img_url = j_handlers.parse_upload_image_json(j)
    if(new_img_url is None):
        return {'success': False,
                'imgur_link': None}
    elif(new_img_url is not None):
        print("Image Link: " + new_img_url) #With file extension
        print("Imgur Link: " + new_img_url[:-4]) #Without file extension
        return {'success': True,
                'imgur_link': new_img_url[:-4]}
