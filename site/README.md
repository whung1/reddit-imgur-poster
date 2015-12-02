## Running the site
First supply your own `auth.ini` files in `app/imgur_backend` and `app/reddit_backend` folders (example `auth_example.ini` files with proper format are provided) with your developer imgur and reddit ids and secrets

Simply run the website using `python run.py`
(after installing necessary libraries through `pip install -r requirements.txt`)

## Unit Tests
Run `python tests_basic.py` or `python -m unittest tests_basic` or likewise for any other test files (e.g. `test_user.py`)

