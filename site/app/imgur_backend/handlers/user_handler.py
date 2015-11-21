"""Methods for handling Imgur User Class
(see models.py in site/app for model)

Holds the access and refresh tokens (if applicable) of a User
and to return authorization headers for user-specific actions"""

from datetime import datetime, timedelta

def access_token_expired(imgur_user, t_limit=3000):
    """Check date access_token was last refreshed
    If it has been past an hour, the access_token
    is expired

    NOTE: Time limit is to be considered expired
    is set to 3000 seconds (50 minutes) by default"""
    time_diff = datetime.now() - imgur_user.last_refresh
    if(time_diff.total_seconds() > t_limit):
        return True # Expired
    else:
        return False # Not expired

def get_access_token(imgur_user):
    return imgur_user.access_token

def set_access_token(imgur_user, new_access_token):
    imgur_user.access_token = new_access_token

def get_refresh_token(imgur_user):
    return imgur_user.refresh_token

def set_refresh_token(imgur_user, new_refresh_token):
    imgur_user.refresh_token = new_refresh_token

def get_last_refresh_time(imgur_user):
    return imgur_user.last_refresh

def set_last_refresh_time(imgur_user, new_datetime=None):
    if (new_datetime is None):
        new_datetime = datetime.datetime.now()

    imgur_user.last_refresh = new_datetime

def get_username(imgur_user):
    return imgur_user.username

def set_username(imgur_user, new_username):
    imgur_user.username = new_username

def get_header(imgur_user, client_id):
    """ Function to get the header for API actions
    Changes depending whether or not the user
    has a valid token with the application

    Returns an authroization header (dictionary)"""
    if(imgur_user is None):
        # User does not have necessary tokens for authorization
        # Return the general header for this application
        return {"Authorization": "Client-ID {0}".format(
                    client_id)}
    else:
        # User has been authorized
        # Return header specific to this user via their access token
        return {"Authorization": "Bearer {0}".format(
                    get_access_token(imgur_user))}
