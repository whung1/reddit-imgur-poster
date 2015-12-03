# reddit-imgur-poster
Ongoing work for mini-website to help posting images on reddit by
automatically uploading file URLs to imgur, then with the provided information, making a post with that newly uploaded rehosted image url

Final Week List (For CS242):
  * COMPLETED:
    * Create basic README.mds
    * Create neat requirements.txt through pipreqs
    * Database (SQLAlchemy)
    * Login
        * Flask-Login re-implementation
            * Handle hack attempts
    * Registration
        * Handling UNIQUE Constraint for SQLITE
    * Delete Account functionality
    * Imgur Portion
        * Refactored user model/handlers
        * Refresh Token Backend
        * Handle exceptions
    * Reddit Portion
        * Reddit Account, Linking and Unlinking
            * Handle exceptions/unusual hack attempts
            * Get rid of storing access tokens for reddit user
        * Reddit Posting
            * Optional Comments
            * Basic Posting
            * Only allow submission with linked reddit account
            * Handle exceptions
            * Handle errors if server is stopped
    * Account Pages
        * Delete account button
        * Navbar inclusion when logged in ONLY
        * Linking template/redirecting reorganization
    * Unit Testing
        * Website User (tests_user.py)
            * Refactoring of unit test helper methods
            * Revamped some unit tests which were reliant on others
            * User Registration unit tests
            * User Delete unit tests
        * Reddit_User model (tests_reddit_user.py)
        * Imgur_User model (tests_imgur_user.py)

  * TO-DO:

12/20 Onwards List:
  * COMPLETED:
  * TO-DO:
    * Seperate test cases into a folder via python import hacks
    * Navbar highlighting active tab (robust method)
    * Decide if we want to stick with PRAW
        * PRAW fix for multi-users (sessions? praw-multithread? hack?)
    * Horizontal parallax UI for submission
    * Utilize "state" portion of OAuth2 authentication
    * Image Uploading
        * Display a small thumbnail of the image uploaded
        * Integrate in multistep process via horizontal parallax
    * Reddit Posting
        * Multistep process via horizontal parallax
        * Subreddit Autocomplete GET (Reddit backend+Javascript?)
    * AJAX submission
        * No more page refreshing(?), as all the content is in body
        * Imgur CAPTCHA handling
        * Reddit CAPTCHA handling
    * Account Pages
        * Display basic info on accounts (karma, etc)
        * Live information grab for imgur and reddit link pages
    * Change to using Flask-WTF-Forms
    * Unit Testing
        * Imgur-backend
        * Reddit-backend

Possible Features List:
  * TO-DO:
    * Image hosting implementation on other sites
