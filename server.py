from flask import Flask, request
import json
import requests

import bayes.bayesbest

app = Flask(__name__)

PAT = '***REMOVED***'

@app.route('/', methods=['GET'])
def handle_verification():
    print "Handling Verification: ->"
    if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
        print "Verification successful!"
        return request.args.get('hub.challenge', '')
    else:
        print "Verification failed!"
        return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def handle_messages():
    print "Handling Messages"
    payload = request.get_data()
    print payload
    b = bayes.bayesbest.Bayes_Classifier()
    for sender, message in messaging_events(payload):
        print "Incoming from %s: %s" % (sender, message)
        tokens = b.tokenize(message)
        if len(tokens) > 0 and tokens[0].lower() == "classify":
            res = b.classify(message)
            send_message(PAT, sender, res)
        elif len(tokens) > 0 and tokens[0].lower() == "reverse:":
            reverse_message = message[::-1]
            send_message(PAT, sender, reverse_message)
        else:
            send_message(PAT, sender, message)
    return "ok"

def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
        else:
            yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text):
    """Send the message text to recipient with id recipient.
    """

    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": token},
        data=json.dumps({
          "recipient": {"id": recipient},
          "message": {"text": text.decode('unicode_escape')}
        }),
        headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text

if __name__ == '__main__':
    app.run()