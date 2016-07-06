"""
This module provides an interface to make HTTP requests to the Facebook page.
"""

import requests

def get(access_token, data):
    """Send get request to Facebook page."""
    r = requests.get(
        "https://graph.facebook.com/v2.6/me/messages",
        params={
            "access_token": access_token
        }
    )
    if r.status_code != requests.codes.ok:
        print r.text

def post(access_token, data):
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

def delete(access_token, data):
    """Send delete request to Facebook page."""
    r = requests.delete(
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
