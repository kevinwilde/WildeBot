from flask import Flask, request
import json

import bot, setup

app = Flask(__name__)


PAT = '***REMOVED***'
PASSWORD = '***REMOVED***'

setup.create_persistent_menu(PAT)
mr_bot = create_bot(PAT)

def create_bot(token):
    return bot.Bot(token) 

@app.route('/', methods=['GET'])
def handle_verification():
    print "Handling Verification"
    if request.args.get('hub.verify_token', '') == PASSWORD:
        print "Verification successful"
        return request.args.get('hub.challenge', '')
    else:
        print "Verification failed"
        return 'Error: Verification failed'

@app.route('/', methods=['POST'])
def handle_messages():
    print "Handling Messages"
    payload = request.get_data()
    for sender, message in messaging_events(payload):
        print "Incoming from %s: %s" % (sender, message)
        mr_bot.act_on_message(sender, message)
    return "ok"

def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the
    provided payload."""
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        # Messages
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')

        # Postbacks
        elif "postback" in event and "payload" in event["postback"]:
            yield event["sender"]["id"], event["postback"]["payload"].encode('unicode_escape')
        
        else:
            yield event["sender"]["id"], "I can't echo this"


if __name__ == '__main__':
    app.run(debug=True)
