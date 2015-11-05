#!/usr/bin/python

""" Interactions with user input in console
TODO: Change to web based
"""

def display_help():
    print("""
    /login          Log onto your account for future actions
    /upload         Upload image onto Imgur
    /h /help        Displays this help menu
    /quit /exit     Exit the console
    """)

def request_pin(client_id):
    print("Please click the following link to validate your imgur account:")
    # Generate the correct url for pin request
    req_resp = "pin"
    state = "anything"
    url = 'https://api.imgur.com/oauth2/authorize?client_id={cid}&response_type={resp}&state={app_state}'
    url = url.format(cid=client_id, resp= req_resp, app_state = state)
    print(url)
    
    return get_input("Your Given Pin Code:")

def get_input(display):
    print(display)
    usr_in = str(raw_input(" - "))
    return usr_in

def request_image_url():
    return get_input("Image URL to upload:")
