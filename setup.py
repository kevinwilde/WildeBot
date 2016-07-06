"""
Set up messenger bot, including creating persistent menu
"""

from . import fb

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
        payload = [
            {
                "payload": "I don't know yet"
            }
        ]
        fb.thread_settings.create_get_started_btn(access_token, payload)
