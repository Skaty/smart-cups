import logging
import requests

from utils import get_commitment_digest

'''
Interfaces with the PTC
'''
API_URL = "http://127.0.0.1:5000{}"

def handle_json_response(r):
    try:
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as err:
        logging.warning("Invalid response!")
        try:
            logging.warning("Got error: {}".format(r.json()['message']))
        except ValueError:
            logging.warning("No error from server!")
        return {}

def create_user():
    '''Creates a new user'''
    r = requests.post(API_URL.format('/users'))
    return handle_json_response(r)

def create_game(uid, num_cups, num_players, r, position):
    '''
    Creates a new cup shuffling game
    Returns: (salt, response)
    '''
    salt, digest = get_commitment_digest(r, position)
    payload = {
        'user_id': str(uid),
        'cups_count': num_cups,
        'players_count': num_players,
        'salt': salt,
        'commitment': digest
    }
    print(payload)
    r = requests.post(API_URL.format('/games'), json=payload)
    return (salt, handle_json_response(r))
