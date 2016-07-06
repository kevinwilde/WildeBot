import json

from . import post

def create_persistent_menu(access_token, menu):
    """Create Persistent Menu."""
    print "Call create_persistent_menu"
    data = json.dumps({
        "setting_type": "call_to_actions",
        "thread_state": "existing_thread",
        "call_to_actions": menu
    })
    post.post_to_fb(access_token, data)

def create_greeting_text(access_token, greeting_text):
    """Create Greeting Text."""
    print "Call create_greeting_text"
    data = json.dumps({
        "setting_type": "greeting",
        "greeting": {
            "text": greeting_text
        }
    })
    post.post_to_fb(access_token, data)

def create_get_started_btn(access_token, payload):
    """Create Greeting Text."""
    print "Call create_greeting_text"
    data = json.dumps({
        "setting_type": "call_to_actions",
        "thread_state": "new_thread",
        "call_to_actions": payload
    })
    post.post_to_fb(access_token, data)
