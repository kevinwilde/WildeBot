import json
import requests

import wildebot.bayes as bayes
import wildebot.games as games

class Bot(object):

    def __init__(self, token):
        self.token = token
        self.bayes_classifier = bayes.BayesClassifier()
        self.ttt_extension = "TTTGame.pickle"
        self.mancala_extension = "MancGame.pickle"

    def act_on_message(self, sender, message):
        """Determine how to respond to message"""
        tokens = self.bayes_classifier.tokenize(message)

        # Greeting
        if len(tokens) > 0 and is_greeting(tokens[0]):
            self.send_message(sender, "Hello")

        # Repeat
        elif len(tokens) > 0 and tokens[0].lower() == "repeat":
            self.send_message(sender, message[len("repeat")+1:])

        # Reverse
        elif len(tokens) > 0 and tokens[0].lower() == "reverse":
            reverse_message = message[::-1]
            self.send_message(sender, reverse_message)

        # Tic Tac Toe
        elif len(tokens) > 1 and tokens[0].lower() == "ttt":
            self.host_ttt_game(sender, tokens)

        # Mancala
        elif len(tokens) > 1 and tokens[0].lower() == "mancala":
            self.host_mancala_game(sender, tokens)

        # Bayes
        else:
            diff = self.bayes_classifier.classify(message)
            self.send_message(sender, str(diff) + " " + self.react(diff))

        return "ok"

    def send_message(self, recipient, text, attachment=None):
        if attachment is not None:
            pass
        else:
            self.send_text_message(recipient, text)

    def send_text_message(self, recipient, text):
        """Send the message text to recipient with id recipient."""
        r = requests.post(
            "https://graph.facebook.com/v2.6/me/messages",
            params={
                "access_token": self.token
            },
            data=json.dumps({
                "recipient": {
                    "id": recipient
                },
                "message": {
                    "text": text.decode('unicode_escape')
                }
            }),
            headers={
                "Content-type": "application/json"
            }
        )
        if r.status_code != requests.codes.ok:
            print r.text

    def react(self, score):
        """Return string based on score
        Positive scores get more positive reactions
        Negative scores get more negative reactions
        """
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

    def host_ttt_game(self, sender, tokens):
        """Tic Tac Toe game hosted on server"""
        if tokens[1].lower() == "new":
            t = games.TicTacToe.TTTBoard()
            self.send_message(sender, str(t) + "\nYou go first")
            t.save_game(sender + self.ttt_extension)
        else:
            try:
                t = games.TicTacToe.TTTBoard.load_game(sender + self.ttt_extension)
                move = int(tokens[1])
                if t.game_over():
                    self.send_message(sender, "Game over\nStart new game with TTT new")
                elif t.turn != 1:
                    self.send_message(sender, "Not your turn yet")
                elif t.legal_move(1, move):
                    t.make_move(1, move)
                    self.send_message(sender, str(t))

                    if t.game_over():
                        if t.has_won(1):
                            self.send_message(sender, "You win!")
                        else:
                            self.send_message(sender, "Cat's game")

                    # Bot responds
                    else:
                        player2 = games.Player.Player(2, games.Player.Player.ABPRUNE, ply=9)
                        ab_move = player2.choose_move(t)
                        t.make_move(2, ab_move)
                        self.send_message(sender, str(t))

                        if t.game_over():
                            if t.has_won(2):
                                self.send_message(sender, "I win!")
                            else:
                                self.send_message(sender, "Cat's game")

                    t.save_game(sender + self.ttt_extension)
                else:
                    self.send_message(sender, "Illegal move")

            except Exception as e:
                print e
                err_msg = "Something went wrong...\nMake sure you are choosing a valid square"
                self.send_message(sender, err_msg)


    def host_mancala_game(self, sender, tokens):
        """Mancala game hosted on server"""
        if tokens[1].lower() == "new":
            m = games.Mancala.MancalaBoard()
            self.send_message(sender, str(m) + "\nYou go first")
            m.save_game(sender + self.mancala_extension)
        else:
            try:
                m = games.Mancala.MancalaBoard.load_game(sender + self.mancala_extension)
                move = int(tokens[1])
                if m.game_over():
                    self.send_message(sender, "Game over\nStart new game with Mancala new")
                elif m.turn != 1:
                    self.send_message(sender, "Not your turn yet")

                else:
                    if m.legal_move(1, move):
                        m.make_move(1, move)
                        self.send_message(sender, str(m))
                    else:
                        self.send_message(sender, "Illegal move")

                # Bot responds
                while m.turn == 2 and not m.game_over():
                    self.send_message(sender, "My turn")
                    player2 = games.Player.Player(2, games.Player.Player.CUSTOM, ply=9)
                    ab_move = player2.choose_move(m)
                    self.send_message(sender, "I choose " + str(ab_move))
                    m.make_move(2, ab_move)
                    self.send_message(sender, str(m))

                if m.turn == 1:
                    self.send_message(sender, "Your turn again")
                elif m.game_over():
                    if m.has_won(1):
                        self.send_message(sender, "You win!")
                    elif m.has_won(2):
                        self.send_message(sender, "I win!")
                    else:
                        self.send_message(sender, "Cat's game")

                m.save_game(sender + self.mancala_extension)

            except Exception as e:
                print e
                err_msg = "Something went wrong...\nMake sure you are choosing a valid square"
                self.send_message(sender, err_msg)



def is_greeting(word):
    """Determines if word is a greeting"""
    greetings = ["hi", "hello", "hey"]
    return word.lower() in greetings
