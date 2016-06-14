from flask import Flask, request
import json
import requests

from globalvars import *
# import bayesbest
# import classdata
from TicTacToe import *
from Player import *


app = Flask(__name__)


@app.route('/', methods=['GET'])
def handle_verification():
    print "Handling Verification: ->"
    if request.args.get('hub.verify_token', '') == password:
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
    for sender, message in messaging_events(payload):
        print "Incoming from %s: %s" % (sender, message)
        # send_message(PAT, sender, message)
        tokens = b.tokenize(message)
        print "Tokens", tokens

        # Classify
        if len(tokens) > 0 and tokens[0].lower() == "classify":
            res = b.classify(tokens[1:])
            send_message(PAT, sender, res)

        # Reverse
        elif len(tokens) > 0 and tokens[0].lower() == "reverse":
            reverse_message = message[::-1]
            send_message(PAT, sender, reverse_message)

        # Tic Tac Toe
        elif (len(tokens) > 1 
            and tokens[0].lower() =="ttt"
            and tokens[1].lower() == "new"):
            t = TTTBoard()
            # player1 = Player(1, Player.HUMAN)
            # player2 = Player(2, Player.ABPRUNE, ply=9)
            # t.hostGame(player1, player2)
            send_message(PAT, sender, str(t) + "\nYou go first")
            t.saveGame(sender + ttt_extension)
        elif (len(tokens) > 1 and tokens[0].lower() =="ttt"):
            try:
                t = TTTBoard()
                t = t.loadGame(sender + ttt_extension)
                move = int(tokens[1])
                if t.hasWon(1) or t.hasWon(2):
                    send_message(PAT, sender, "Game over\nStart new game with TTT new")
                elif t.legalMove(1, move):
                    t.makeMove(1, move)
                    send_message(PAT, sender, str(t))
                    if t.hasWon(1):
                        winner = 1
                        send_message(PAT, sender, "You win!")

                    # Bot responds
                    player2 = Player(2, Player.ABPRUNE, ply=9)
                    ab_move = player2.chooseMove(t)
                    t.makeMove(2, ab_move)
                    send_message(PAT, sender, str(t))
                    if t.hasWon(2):
                        winner = 2
                        send_message(PAT, sender, "I win!")
                    
                    t.saveGame(sender + ttt_extension)
                else:
                    send_message(PAT, sender, "Illegal move")

            except Exception as e:
                print e
                err_msg = "Something went wrong...\nMake sure you are choosing a valid square"
                send_message(PAT, sender, err_msg)

        # Echo
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
    app.run(debug=True)
