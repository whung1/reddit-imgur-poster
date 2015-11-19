#!/usr/bin/python
import json
import pprint

"""
Helper functions for imgur_handlers.py functions to parse
received JSON and give proper output or errors
"""

# TODO: Change prints to web output
def parse_user_token_json(j):
    """ 
    Helper function for get_user_token to give proper
    response to user depending on JSON response to access token from
    user given pin

    Returns dict indicating success and
    with the access_token and refresh_token respectively
    or error if authorization was not successful
    """
    if('access_token' in j and 'refresh_token' in j):
        return {'success': True,
                'access_token': j['access_token'], 
                'refresh_token': j['refresh_token'],
                'username': j['account_username']}
    else:
        return {'success': False,
                'error': throw_error(j)}

def parse_upload_image_json(j):
    """ Helper function for upload_image
    to parse the JSON response and give the proper
    output

    Returns dict detailing success and 
    uploaded imgur_url or error
    """
    success = j['success']
    if(success == True):
        # Return image link
        # TODO: check if needed to return any specific descriptors

        return {'success': True,
                'imgur_url': j['data']['link'][:-4]}
    else:
        return {'success': False,
                'error': throw_error(j)}


# Error Handling Functions
def throw_error(j):
    status = get_status_code(j)
    j_error = ""
    if('data' in j and 'error' in j['data']):
        j_error = j['data']['error']
    return str(status + " - " + j_error)

def get_status_code(j):
    if('success' not in j):
        return "Malformed JSON Error?"
    
    status = int(j['status'])
    codes = {
            200: "[SUCCESS]",
            400: "[ERROR] Incorrect or missing parameters",# Image upload fail, etc
            401: "[ERROR] Requires or missing proper user authorization", # Either need OAuth credentials or they expired
            403: "[ERROR] Forbidden, incorrect/invalid access", # Check API credits, OAuth headers, and validity of tokens/secrets
            404: "[ERROR] Requested resource does not exist",
            429: "[ERROR] Hit rate limit on application or user",
            500: "[ERROR] Internal Error"
            }
    return codes.get(status, "[UNHANDLED ERROR]")

