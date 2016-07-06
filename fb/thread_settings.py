"""
This module provides an interface to the Facebook Thread Settings API.
"""

import json

from . import fb_request

def create_greeting_text(access_token, greeting_text):
    """Create Greeting Text."""
    data = json.dumps({
        "setting_type": "greeting",
        "greeting": {
            "text": greeting_text
        }
    })
    fb_request.post(access_token, data)

def create_persistent_menu(access_token, menu):
    """Create Persistent Menu."""
    data = json.dumps({
        "setting_type": "call_to_actions",
        "thread_state": "existing_thread",
        "call_to_actions": menu
    })
    fb_request.post(access_token, data)

def delete_persistent_menu(access_token):
    """Delete Persistent Menu."""
    data = json.dumps({
        "setting_type": "call_to_actions",
        "thread_state": "existing_thread"
    })
    fb_request.delete(access_token, data)

def create_get_started_btn(access_token, payload):
    """Create Get Started button."""
    data = json.dumps({
        "setting_type": "call_to_actions",
        "thread_state": "new_thread",
        "call_to_actions": payload
    })
    fb_request.post(access_token, data)

def delete_get_started_btn(access_token):
    """Delete Get Started button."""
    data = json.dumps({
        "setting_type": "call_to_actions",
        "thread_state": "new_thread"
    })
    fb_request.delete(access_token, data)
