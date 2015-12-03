import os
import ConfigParser

from flask import flash
import praw
import praw.errors


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

def get_authorize_url(r, 
        scope = "identity mysubreddits submit"):
    '''Assuming setup() has been run
    on r (Reddit) object, get an authorize
    url for user to click
    '''
    # TODO: Generate meaningful state
    state = "anything"
    return r.get_authorize_url(state, scope, refreshable=True)

def exchange_for_tokens(access_information):
    '''
    '''
    return None

def establish_oauth(r, reddit_usr, 
        scope = "identity mysubreddits submit"):
    if(r.is_oauth_session() == True):
        return True
    if (reddit_usr is None):
        return False
    else:
        try:
            # TODO: Check if access tokens
            # and refresh tokens are changed
            info = r.refresh_access_information(
                    refresh_token=reddit_usr.refresh_token)
            print("Refreshed access info")
        except praw.errors.HTTPException as e:
            exc = e._raw
            flash(exc.status_code, "danger")
        except praw.errors.OAuthInvalidToken:
            flash("Invalid OAuth Token", "danger")
        return r.is_oauth_session()

def submit_post_and_comment(r, reddit_usr, args):
    """Function to verify oauth of current user
    and submit the post with the given url, and then
    add a comment to the post

    Assumes args is a dictionary with subreddit,
    title, url, and comment (optional)"""
    subreddit = args['subreddit']
    title = args['title']
    url = args['url']
    comment = args['comment']
    # TODO: Captcha Handling
    if(r.is_oauth_session()):
        # submit(subreddit, title, text=None, url=None, captcha=None, save=None, send_replies=None, resubmit=None)
        try:
            submission = r.submit(subreddit = subreddit, 
                    title = title, 
                    text = None,
                    url = url,
                    raise_captcha_exception=True)
            try:
                if (comment != ""):
                    submission.add_comment(comment)
                    #TODO: Add exceptions
                return submission.short_link
            except Exception as e:
                flash(e, "danger")
        except praw.errors.InvalidCaptcha as c:
            flash("Invalid Captcha", "danger")
        except Exception as e:
            flash(e, "danger")
        return "fail"
    else:
        return "flase"


def setup():
    r = praw.Reddit("Reddit Img Poster OAuth2")
    client_id = get_client_id()
    client_secret=get_client_secret()
    redirect_uri = get_redirect_uri()
    r.set_oauth_app_info(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri)
    return r

