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
        * Refresh Token Backend
        * Handle exceptions
    * Reddit Portion
        * Reddit Account, Linking and Unlinking
            * Handle exceptions/unusual hack attempts
        * Reddit Posting
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
            * Revamped some unit tests which were reliant on others
            * Account Registration unit tests
            * Account Delete unit tests

  * TO-DO:
    * Reddit Portion
        * Reddit Posting
            * Optional Comments
    * Flask-WTF-Forms change
    * Unit Testing
        * Imgur-backend
        * Reddit-backend
    * Account Pages (IN PROGRESS)
        * Display basic info on accounts and redirect to linking pages
        * Live information grab for imgur and reddit link pages

12/20 Onwards List:
  * COMPLETED:
  * TO-DO:
    * Seperate test cases into a folder via python import hacks
    * Navbar highlighting active tab (robust method)
    * Decide if we want to stick with PRAW
        * PRAW fix for multi-users (sessions? praw-multithread? hack?)
        * Get rid of storing access tokens for reddit user
    * Better UI for submission
    * Utilize "state" portion of OAuth2 authentication
    * Reddit Posting
        * Multistep process
        * Subreddit Autocomplete GET (Reddit backend+Javascript?)
    * AJAX submission
        * No more page refresh
        * Imgur CAPTCHA handling
        * Reddit CAPTCHA handling

Possible Features List:
  * TO-DO:
    * Image hosting implementation of other sites
