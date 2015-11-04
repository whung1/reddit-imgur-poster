#!/usr/bin/python

from handlers.imgur import ImgurHandler
from viewers.imgurviewer import ImgurViewer

CLIENT_ID = 'f38a75f28f64788'
CLIENT_SECRET = '57a3f6a1b5ff9ea71e826fceb32c97a606672669'

ImgurHandler.login('blah','blah')
ImgurHandler.get_auth_header(CLIENT_ID)

# Get Imgur account pin
ImgurViewer.request_pin()
