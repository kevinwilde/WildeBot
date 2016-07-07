"""
This module provides an interface to the Facebook Thread Settings API.
"""

import json

def create_thread_setting(access_token, data):
    """Create thread setting via post request to Facebook page."""
    r = requests.post(
        "https://graph.facebook.com/v2.6/me/thread_settings",
        params={
            "access_token": access_token
        },
        data=data,
        headers={
            "Content-type": "application/json"
        }
    )
    if r.status_code != requests.codes.ok:
        print r.text

def delete_thread_setting(access_token, data):
    """Delete thread setting via delete request to Facebook page."""
    r = requests.delete(
        "https://graph.facebook.com/v2.6/me/thread_settings",
        params={
            "access_token": access_token
        },
        data=data,
        headers={
            "Content-type": "application/json"
        }
    )
    if r.status_code != requests.codes.ok:
        print r.text

def create_greeting_text(access_token, greeting_text):
    """Create Greeting Text."""
    data = json.dumps({
        "setting_type": "greeting",
        "greeting": {
            "text": greeting_text
        }
    })
    create_thread_setting(access_token, data)

def create_persistent_menu(access_token, menu):
    """Create Persistent Menu."""
    data = json.dumps({
        "setting_type": "call_to_actions",
        "thread_state": "existing_thread",
        "call_to_actions": menu
    })
    create_thread_setting(access_token, data)

def delete_persistent_menu(access_token):
    """Delete Persistent Menu."""
    data = json.dumps({
        "setting_type": "call_to_actions",
        "thread_state": "existing_thread"
    })
    delete_thread_setting(access_token, data)

def create_get_started_btn(access_token, payload):
    """Create Get Started button."""
    data = json.dumps({
        "setting_type": "call_to_actions",
        "thread_state": "new_thread",
        "call_to_actions": payload
    })
    create_thread_setting(access_token, data)

def delete_get_started_btn(access_token):
    """Delete Get Started button."""
    data = json.dumps({
        "setting_type": "call_to_actions",
        "thread_state": "new_thread"
    })
    delete_thread_setting(access_token, data)
