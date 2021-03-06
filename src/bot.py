import bayes
import fb
import games

TTT_EXTENSION = "TTTGame.pickle"
MANCALA_EXTENSION = "MancGame.pickle"

class Bot(object):

    def __init__(self, token):
        self.token = token
        self.bayes_classifier = bayes.BayesClassifier()

    def act_on_message(self, sender, message):
        fb.send_api.mark_seen(self.token, sender)
        tokens = self.bayes_classifier.tokenize(message)
        # Greeting
        if len(tokens) > 0 and is_greeting(tokens[0]):
            fb.send_api.send_text_message(self.token, sender, "Hello")
        # Help
        elif message.lower() == "help" or message.lower() == "get started":
            self.send_help_message(sender)
        # Repeat
        elif len(tokens) > 0 and tokens[0].lower() == "repeat":
            fb.send_api.send_text_message(self.token, sender, message[len("repeat")+1:])
        # Reverse
        elif len(tokens) > 0 and tokens[0].lower() == "reverse":
            reverse_message = message[::-1]
            fb.send_api.send_text_message(self.token, sender, reverse_message)
        # Tic Tac Toe
        elif len(tokens) > 1 and tokens[0].lower() == "ttt":
            self.host_ttt_game(sender, tokens)
        # Mancala
        elif len(tokens) > 1 and tokens[0].lower() == "mancala":
            self.host_mancala_game(sender, tokens)
        # Bayes
        else:
            diff = self.bayes_classifier.classify(message)
            fb.send_api.send_text_message(self.token, sender, react(diff))

    def send_help_message(self, sender):
        msg = "Hi there!"
        fb.send_api.send_text_message(self.token, sender, msg)
        msg = ("I am an artificially intelligent Facebook Messenger bot. You "
               "can play against it in Tic-Tac-Toe or Mancala by using the "
               "menu in the bottom left corner.")
        fb.send_api.send_text_message(self.token, sender, msg)
        msg = ("You can also talk to me, and I will react to what you say "
               "based on how nice (or mean) I think your message is. I can't "
               "really hold a conversation, but if you want to chat more feel "
               "free to message https://m.me/wildekevin")
        fb.send_api.send_text_message(self.token, sender, msg)

    def host_ttt_game(self, sender, tokens):
        """Tic Tac Toe game hosted on server"""
        if tokens[1].lower() == "new":
            t = games.TicTacToe.TTTBoard()
            quick_replies = create_quick_replies("TTT", t.legal_moves(1))
            fb.send_api.send_text_message(self.token, sender, str(t))
            fb.send_api.send_quick_replies(self.token, sender, "Your turn", quick_replies)
            t.save_game(sender + TTT_EXTENSION)
        else:
            try:
                t = games.TicTacToe.TTTBoard.load_game(sender + TTT_EXTENSION)
            except IOError:
                err_msg = "No active TicTacToe game. Start a new game to play."
                fb.send_api.send_text_message(self.token, sender, err_msg)
            else:
                move = int(tokens[1])
                if t.game_over():
                    fb.send_api.send_text_message(self.token, sender, "Game over\nStart new game with TTT new")
                elif t.turn != 1:
                    fb.send_api.send_text_message(self.token, sender, "Not your turn yet")
                elif t.legal_move(1, move):
                    t.make_move(1, move)
                    fb.send_api.send_text_message(self.token, sender, str(t))

                    if t.game_over():
                        if t.has_won(1):
                            fb.send_api.send_text_message(self.token, sender, "You win!")
                        else:
                            fb.send_api.send_text_message(self.token, sender, "Cat's game")

                    # Bot responds
                    else:
                        player2 = games.Player.Player(2, games.Player.Player.ABPRUNE, ply=9)
                        ab_move = player2.choose_move(t)
                        fb.send_api.send_text_message(self.token, sender, "I choose " + str(ab_move))
                        t.make_move(2, ab_move)
                        fb.send_api.send_text_message(self.token, sender, str(t))

                        if t.game_over():
                            if t.has_won(2):
                                fb.send_api.send_text_message(self.token, sender, "I win!")
                            else:
                                fb.send_api.send_text_message(self.token, sender, "Cat's game")
                        else:
                            quick_replies = create_quick_replies("TTT", t.legal_moves(1))
                            fb.send_api.send_quick_replies(self.token, sender, "Your turn", quick_replies)

                    t.save_game(sender + TTT_EXTENSION)
                else:
                    fb.send_api.send_text_message(self.token, sender, "Illegal move")


    def host_mancala_game(self, sender, tokens):
        """Mancala game hosted on server"""
        if tokens[1].lower() == "new":
            m = games.Mancala.MancalaBoard()
            quick_replies = create_quick_replies("Mancala", m.legal_moves(1))
            fb.send_api.send_text_message(self.token, sender, str(m))
            fb.send_api.send_quick_replies(self.token, sender, "Your turn", quick_replies)
            m.save_game(sender + MANCALA_EXTENSION)
        else:
            try:
                m = games.Mancala.MancalaBoard.load_game(sender + MANCALA_EXTENSION)
            except IOError:
                err_msg = "No active Mancala game. Start a new game to play."
                fb.send_api.send_text_message(self.token, sender, err_msg)
            else:
                move = int(tokens[1])
                if m.game_over():
                    fb.send_api.send_text_message(self.token, sender, "Game over\nStart new game with Mancala new")
                elif m.turn != 1:
                    fb.send_api.send_text_message(self.token, sender, "Not your turn yet")
                else:
                    if m.legal_move(1, move):
                        m.make_move(1, move)
                        fb.send_api.send_text_message(self.token, sender, str(m))
                    else:
                        fb.send_api.send_text_message(self.token, sender, "Illegal move")

                # Bot responds
                while m.turn == 2 and not m.game_over():
                    fb.send_api.send_text_message(self.token, sender, "My turn")
                    player2 = games.Player.Player(2, games.Player.Player.CUSTOM, ply=9)
                    ab_move = player2.choose_move(m)
                    fb.send_api.send_text_message(self.token, sender, "I choose " + str(ab_move))
                    m.make_move(2, ab_move)
                    fb.send_api.send_text_message(self.token, sender, str(m))

                if m.game_over():
                    if m.has_won(1):
                        fb.send_api.send_text_message(self.token, sender, "You win!")
                    elif m.has_won(2):
                        fb.send_api.send_text_message(self.token, sender, "I win!")
                    else:
                        fb.send_api.send_text_message(self.token, sender, "Cat's game")
                elif m.turn == 1:
                    quick_replies = create_quick_replies("Mancala", m.legal_moves(1))
                    fb.send_api.send_quick_replies(self.token, sender, "Your turn", quick_replies)

                m.save_game(sender + MANCALA_EXTENSION)



def is_greeting(word):
    greetings = ["hi", "hello", "hey"]
    return word.lower() in greetings

def react(score):
    """Return string based on score.

    Positive scores get more positive reactions.
    Negative scores get more negative reactions.
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
        "What an amazing thing to hear! The world sure could use more people like you" #11
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

def create_quick_replies(game, legal_moves):
    """Create quick replies for user to make next move."""
    quick_replies = []
    for move in legal_moves:
        quick_reply = {
            "content_type": "text",
            "title": move,
            "payload": game + " " + str(move)
        }
        quick_replies.append(quick_reply)
    return quick_replies
