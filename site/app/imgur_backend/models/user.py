# TODO: Convert this to web-based database structure
class User:
    """ Imgur User Class
    Holds the access and refresh tokens (if applicable) of a User
    and returns the necessary header for any action
    NOTE: Header will be set as if the user does not exist initially
    """
    def __init__(self, client_id, username =None, access_token=None, refresh_token=None):
        self.client_id = client_id
        self.access_token = access_token
        self.refresh_token = refresh_token 

    def update_user(self, tokens):
        if(tokens is not None):
            self.access_token = tokens[0]
            self.refresh_token = tokens[1]
            self.username = tokens[2]
            print("You are logged in as " + self.username)

    def get_header(self):
        """ Function to get the header for API actions
        Changes depending whether or not the user
        has a valid token with the application
        
        Returns a dict header
        """
        if(self.client_id is None):
            print("[ERROR] Nonexistent client_id for user")
            return None

        if(self.access_token is not None
                and self.refresh_token is not None):
            # User has been authorized
            # Return header specific to this user
            return {"Authorization": "Bearer {0}".format(
                    self.access_token)}

        else:
            # User does not have necessary tokens for authorization
            # Return general header for this application
            return {"Authorization": "Client-ID {0}".format(
                    self.client_id)}
            
