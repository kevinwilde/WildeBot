def create_persistent_menu(token):
    """Create Persistent Menu"""
    print "Call create_persistent_menu"
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