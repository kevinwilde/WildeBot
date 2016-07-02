from flask import Flask, request
import json
import requests

from globalvars import *
from games.Mancala import *
from games.Player import *
from games.TicTacToe import *


app = Flask(__name__)


@app.route('/', methods=['GET'])
def handle_verification():
    print "Handling Verification: ->"
    if request.args.get('hub.verify_token', '') == PASSWORD:
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
        tokens = b.tokenize(message)

        # Greeting
        if len(tokens) > 0 and is_greeting(tokens[0]):
            send_message(PAT, sender, "Hello")

        # Repeat
        elif len(tokens) > 0 and tokens[0].lower() == "repeat":
            send_message(PAT, sender, message[len("repeat")+1:])

        # Reverse
        elif len(tokens) > 0 and tokens[0].lower() == "reverse":
            reverse_message = message[::-1]
            send_message(PAT, sender, reverse_message)

        # Tic Tac Toe
        elif len(tokens) > 1 and tokens[0].lower() =="ttt":
            host_ttt_game(sender, tokens)

        # Mancala
        elif len(tokens) > 1 and tokens[0].lower() =="mancala":
            host_mancala_game(sender, tokens)

        # Bayes
        else:
            diff = b.classify(message)
            send_message(PAT, sender, str(diff) + " " + react(diff))

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


def send_message(token, recipient, text):
    """Send the message text to recipient with id recipient."""
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": token},
        data=json.dumps({
          "recipient": {"id": recipient},
          "message": {"text": text.decode('unicode_escape')}
        }),
        headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text

def create_persistent_menu(token):
    """Create Persistent Menu"""
    print "CALL CREATE_PERSISTENT_MENU"
    r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings",
        params={"access_token": token},
        data=json.dumps({
          "setting_type" : "call_to_actions",
          "thread_state" : "existing_thread",
          "call_to_actions": [
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
              "title": "View Website",
              "url": "https://www.facebook.com/kevinwildebot"
            }
          ]
        }),
        headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text


def is_greeting(word):
    """Determines if word is a greeting"""
    greetings = ["hi", "hello", "hey"]
    return word.lower() in greetings


def host_ttt_game(sender, tokens):
    """Tic Tac Toe game hosted on server"""
    if tokens[1].lower() == "new":
        t = TTTBoard()
        send_message(PAT, sender, str(t) + "\nYou go first")
        t.save_game(sender + TTT_EXTENSION)
    else:
        try:
            t = TTTBoard.load_game(sender + TTT_EXTENSION)
            move = int(tokens[1])
            if t.game_over():
                send_message(PAT, sender, "Game over\nStart new game with TTT new")
            elif t.turn != 1:
                send_message(PAT, sender, "Not your turn yet")
            elif t.legal_move(1, move):
                t.make_move(1, move)
                send_message(PAT, sender, str(t))
                
                if t.game_over():
                    if t.has_won(1):
                        send_message(PAT, sender, "You win!")
                    else:
                        send_message(PAT, sender, "Cat's game")

                # Bot responds
                else:
                    player2 = Player(2, Player.ABPRUNE, ply=9)
                    ab_move = player2.choose_move(t)
                    t.make_move(2, ab_move)
                    send_message(PAT, sender, str(t))
                    
                    if t.game_over():
                        if t.has_won(2):
                            send_message(PAT, sender, "I win!")
                        else:
                            send_message(PAT, sender, "Cat's game")
                
                t.save_game(sender + TTT_EXTENSION)
            else:
                send_message(PAT, sender, "Illegal move")

        except Exception as e:
            print e
            err_msg = "Something went wrong...\nMake sure you are choosing a valid square"
            send_message(PAT, sender, err_msg)


def host_mancala_game(sender, tokens):
    """Mancala game hosted on server"""
    if tokens[1].lower() == "new":
        m = MancalaBoard()
        send_message(PAT, sender, str(m) + "\nYou go first")
        m.save_game(sender + MANCALA_EXTENSION)
    else:
        try:
            m = MancalaBoard.load_game(sender + MANCALA_EXTENSION)
            move = int(tokens[1])
            if m.game_over():
                send_message(PAT, sender, "Game over\nStart new game with Mancala new")
            elif m.turn != 1:
                send_message(PAT, sender, "Not your turn yet")

            else:
                if m.legal_move(1, move):
                    m.make_move(1, move)
                    send_message(PAT, sender, str(m))
                else:
                    send_message(PAT, sender, "Illegal move")

            # Bot responds
            while m.turn == 2  and not m.game_over():
                send_message(PAT, sender, "My turn")
                player2 = Player(2, Player.CUSTOM, ply=9)
                ab_move = player2.choose_move(m)
                send_message(PAT, sender, "I choose " + str(ab_move))
                m.make_move(2, ab_move)
                send_message(PAT, sender, str(m))

            if m.turn == 1:
                send_message(PAT, sender, "Your turn again")
            elif m.game_over():
                if m.has_won(1):
                    send_message(PAT, sender, "You win!")
                elif m.has_won(2):
                    send_message(PAT, sender, "I win!")
                else:
                    send_message(PAT, sender, "Cat's game")

            m.save_game(sender + MANCALA_EXTENSION)

        except Exception as e:
            print e
            err_msg = "Something went wrong...\nMake sure you are choosing a valid square"
            send_message(PAT, sender, err_msg)

def react(score):
    """Return string based on score
    Positive scores get more positive reactions
    Negative scores get more negative reactions"""
    reactions = [
        "I don't ever want to hear from you again", #0
        "You actually suck", #1
        "That is incredibly mean", #2
        "I don't appreciate you saying that", #3
        "Please find something nicer to say", #4
        "K", #5
        "Ok", #6
        "Is that a compliment?", #7
        "Thanks", #8
        "You are the best :)", #9
        "You just made my day! Thank you!", #10
        "What an amazing thing to hear! The world sure could use more people like you", #11
        ]
    if score < -12:
        return reactions[0]
    elif score < -10:
        return reactions[1]
    elif score < -8:
        return reactions[2]
    elif score < -6:
        return reactions[3]
    elif score < -4:
        return reactions[4]
    elif score < -2:
        return reactions[5]
    elif score < 2:
        return reactions[6]
    elif score < 4:
        return reactions[7]
    elif score < 6:
        return reactions[8]
    elif score < 8:
        return reactions[9]
    elif score < 10:
        return reactions[10]
    else:
        return reactions[11]


create_persistent_menu(PAT)

if __name__ == '__main__':
    app.run(debug=True)
