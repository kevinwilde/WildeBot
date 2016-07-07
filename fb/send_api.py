"""
This module provides an interface to the Facebook Send API.
"""

import json

def send_message(access_token, data):
    """Send message via post request to Facebook page."""
    r = requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
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

def set_sender_action(access_token, recipient, sender_action):
    """Set sender action."""
    data = json.dumps({
        "recipient": {
            "id": recipient
        },
        "sender_action": sender_action
    })
    send_message(access_token, data)

def mark_seen(access_token, recipient):
    set_sender_action(access_token, recipient, "mark_seen")

def typing_on(access_token, recipient):
    set_sender_action(access_token, recipient, "typing_on")

def typing_off(access_token, recipient):
    set_sender_action(access_token, recipient, "typing_off")

def send_text_message(access_token, recipient, text):
    """Send the message text to recipient with id recipient."""
    data = json.dumps({
        "recipient": {
            "id": recipient
        },
        "message": {
            "text": text.decode('unicode_escape')
        }
    })
    send_message(access_token, data)

def send_attachment(access_token, recipient, attachment_type, attachment_url):
    data = json.dumps({
        "recipient": {
            "id": recipient
        },
        "message": {
            "attachment": {
                "type": attachment_type,
                "payload": {
                    "url": attachment_url
                }
            }
        }
    })
    send_message(access_token, data)

def send_generic_template(access_token, recipient, elements):
    data = json.dumps({
        "recipient": {
            "id": recipient
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements
                }
            }
        }
    })
    send_message(access_token, data)

def send_button(access_token, recipient, text, buttons):
    data = json.dumps({
        "recipient": {
            "id": recipient
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text,
                    "buttons": buttons
                }
            }
        }
    })
    send_message(access_token, data)

def send_quick_replies(access_token, recipient, text, quick_replies):
    data = json.dumps({
        "recipient": {
            "id": recipient
        },
        "message": {
            "text": text,
            "quick_replies": quick_replies
        }
    })
    send_message(access_token, data)
