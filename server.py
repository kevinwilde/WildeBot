"""
This module defines a server for a Facebook Messenger bot.
"""

import json
import os
import threading
from flask import Flask, request

import bot
import fb

app = Flask(__name__)
PAGE_ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']
PASSWORD = os.environ['PASSWORD']
MESSENGER_BOT = bot.Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def handle_verification():
    """Handle verification."""
    if request.args.get('hub.verify_token', '') == PASSWORD:
        return request.args.get('hub.challenge', '')
    else:
        return 'Error: Verification failed'

@app.route('/', methods=['POST'])
def handle_messages():
    """Handle messages."""
    payload = request.get_data()
    for (mid, sender, message) in messaging_events(payload):
        print "Incoming from %s: %s" % (sender, message)
        # print mid
        thread = threading.Thread(target=MESSENGER_BOT.act_on_message, args=(mid, sender, message))
        thread.start()
    return "ok"

def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the provided
    payload.
    """
    data = json.loads(payload)
    message_events = data["entry"][0]["messaging"]
    for event in message_events:
        if is_quick_reply(event):
            yield decipher_quick_reply(event)
        elif is_postback(event):
            yield decipher_postback(event)
        elif is_text_message(event):
            yield decipher_text_message(event)
        else:
            yield decipher_unknown(event)

def is_quick_reply(event):
    return "message" in event and "quick_reply" in event["message"]

def is_postback(event):
    return "postback" in event and "payload" in event["postback"]

def is_text_message(event):
    return "message" in event and "text" in event["message"]

def decipher_quick_reply(event):
    return (event["message"]["mid"],
            event["sender"]["id"],
            event["message"]["quick_reply"]["payload"].encode('unicode_escape'))

def decipher_postback(event):
    return (event["sender"]["id"] + event["timestamp"],
            event["sender"]["id"],
            event["postback"]["payload"].encode('unicode_escape'))

def decipher_text_message(event):
    return (event["message"]["mid"],
            event["sender"]["id"],
            event["message"]["text"].encode('unicode_escape'))

def decipher_unknown(event):
    return (event["sender"]["id"] + event["timestamp"],
            event["sender"]["id"],
            "I can't handle this")

def initialize(access_token, greeting_text=True, persistent_menu=True,
               get_started_btn=True):
    """Initialize bot according to arguments passed."""
    fb.thread_settings.delete_persistent_menu(access_token)
    fb.thread_settings.delete_get_started_btn(access_token)
    if greeting_text:
        fb.thread_settings.create_greeting_text(access_token, "Greetings!")
    if persistent_menu:
        menu = [
            {
                "type": "postback",
                "title": "Play Mancala",
                "payload": "Mancala new"
            },
            {
                "type": "postback",
                "title": "Play TicTacToe",
                "payload": "TTT new"
            },
            {
                "type": "web_url",
                "title": "View Facebook Page",
                "url": "https://www.facebook.com/kevinwildebot"
            }
        ]
        fb.thread_settings.create_persistent_menu(access_token, menu)
    if get_started_btn:
        payload = [{"payload": "I don't know yet"}]
        fb.thread_settings.create_get_started_btn(access_token, payload)

initialize(PAGE_ACCESS_TOKEN)

if __name__ == '__main__':
    app.run()
