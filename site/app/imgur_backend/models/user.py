""" 
Methods for Imgur User Class (see models.py in site/app for model)
Holds the access and refresh tokens (if applicable) of a User
and returns the necessary header for any action
"""

def access_token_expired(imgur_user):
    '''Check date access_token was last refreshed
    If it has been past an hour, the access_token
    is expired
    '''
    # TODO: Implementation
    return True

def access_token_is_valid(imgur_user):
    if(access_token_expired(imgur_user)):
        # TODO: Refresh the access token with refresh token
        return True
    return True

def get_header(imgur_user, client_id):
    """ Function to get the header for API actions
    Changes depending whether or not the user
    has a valid token with the application
        
    Returns a dict header
    """
    if(imgur_user is None):
        # User does not have necessary tokens for authorization
        # Return the general header for this application
        return {"Authorization": "Client-ID {0}".format(
                    client_id)}
    else:
        # TODO: Check refresh time and use refresh token
        # User has been authorized
        # Return header specific to this user
        return {"Authorization": "Bearer {0}".format(
                    imgur_user.access_token)}
