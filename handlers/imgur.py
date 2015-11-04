#!/usr/bin/python
import base64
import json
import requests

from base64 import b64encode

class ImgurHandler:
    'Imgur Handler Static Class'
    
    @staticmethod
    def login(username, pwd):
        print('Username: ' + username + ', password: '  + pwd)
    
    @staticmethod
    def request_pin(client_id, client_secret):
        url = 'https://api.imgur.com/oauth2/authorize?client_id={cid}&response_type={resp}&state={app_state}'
        print(url)


    @staticmethod
    def get_auth_header(client_id):
        header = 'Authorization: Client-ID ' + client_id
        print(header)
        return header
