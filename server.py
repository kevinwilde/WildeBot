"""
This module defines a server for a Facebook Messenger bot.
"""

import json
import os
from flask import Flask, request

import bot
import fb

app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']
PASSWORD = os.environ['PASSWORD']

MESSENGER_BOT = bot.Bot(PAGE_ACCESS_TOKEN)

initialize(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def handle_verification():
    """Handle verification."""
    print "Handling Verification"
    if request.args.get('hub.verify_token', '') == PASSWORD:
        print "Verification successful"
        return request.args.get('hub.challenge', '')
    else:
        print "Verification failed"
        return 'Error: Verification failed'

@app.route('/', methods=['POST'])
def handle_messages():
    """Handle messages."""
    payload = request.get_data()
    for sender, message in messaging_events(payload):
        print "Incoming from %s: %s" % (sender, message)
        MESSENGER_BOT.act_on_message(sender, message)
    return "ok"

def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the provided
    payload.
    """
    data = json.loads(payload)
    message_events = data["entry"][0]["messaging"]
    for event in message_events:
        # Messages
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')

        # Postbacks
        elif "postback" in event and "payload" in event["postback"]:
            yield event["sender"]["id"], event["postback"]["payload"].encode('unicode_escape')

        else:
            yield event["sender"]["id"], "I can't echo this"

def initialize(access_token, persistent_menu=True, greeting_text=True,
               get_started_btn=True):
    """Initialize bot according to arguments passed"""
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
    if greeting_text:
        fb.thread_settings.create_greeting_text(access_token, "Greetings!")
    if get_started_btn:
        payload = [{"payload": "I don't know yet"}]
        fb.thread_settings.create_get_started_btn(access_token, payload)

if __name__ == '__main__':
    app.run(debug=True)
