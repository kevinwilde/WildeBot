"""
This module defines a function which sends a post request to the Facebook page.
"""

import requests

def post_to_fb(access_token, data):
    """Send post request to Facebook page."""
    r = requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params={
            "access_token": access_token
        },
        data=data,
        headers={
            "Content-type": "application/json"
        }
    )
    if r.status_code != requests.codes.ok:
        print r.text
