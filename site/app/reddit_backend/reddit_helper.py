import praw
import os
import ConfigParser

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

def get_redirect_uri():
    return get_credentials('redirect_uri')

def get_authorize_url(r):
    '''Assuming setup() has been run
    on r (Reddit) object, get an authorize
    url for user to click
    '''
    # TODO: Generate meaningful state
    state = "anything"
    return r.get_authorize_url(state, refreshable=True)

def exchange_for_tokens(access_information):
    '''
    '''
    return None

def reestablish_oauth(r, reddit_usr):
    if (reddit_usr is None):
        return False
    else:
        r.set_access_credentials('identity',
                                reddit_usr.access_token,
                                reddit_usr.refresh_token)
        return r.is_oauth_session()

def setup():
    r = praw.Reddit("Reddit Img Poster OAuth2")
    client_id = get_client_id()
    client_secret=get_client_secret()
    redirect_uri = get_redirect_uri()
    r.set_oauth_app_info(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri)
    return r

