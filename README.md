# WildeBot

This is an artificially intelligent bot for Facebook Messenger. Feel free to
[message it] (https://m.me/kevinwildebot) and like the [Facebook page]
(https://facebook.com/kevinwildebot)!!

The basic setup was constructed with help from [this tutorial]
(http://tsaprailis.com/2016/06/02/How-to-build-and-deploy-a-Facebook-Messenger-bot-with-Python-and-Flask-a-tutorial/).

### To Do
* ~~Use Twitter Naive Bayes classifier~~ Makes app too big
* Move to postgres database instead of pickling files
* Handle each message in own thread? How would this affect if user sent a second
move while bot was still thinking
* 15 second limit? Fix with message_deliveries?
