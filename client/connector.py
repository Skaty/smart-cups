from urllib.parse import urljoin

import logging
import requests

from utils import get_commitment_digest

'''
Interfaces with the PTC
'''
API_URL = 'http://127.0.0.1:5000'

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
    r = requests.post(urljoin(API_URL, 'users'))
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

    r = requests.post(urljoin(API_URL, 'games'), json=payload)
    return (salt, handle_json_response(r))

def get_game(gid):
    '''
    Retrieves a game, given a game ID
    '''
    urn = '/'.join(['games', str(gid)])
    r = requests.get(urljoin(API_URL, urn))
    return handle_json_response(r)

def commit_game(gid, uid, r, guess):
    '''
    Bet on an ongoing cup shuffling game
    Returns: (salt, response)
    '''
    salt, commit = get_commitment_digest(r, guess)
    urn = '/'.join(['games', str(gid), 'commit'])

    payload = {
        'user_id': uid,
        'commitment': commit
    }

    r = requests.post(urljoin(API_URL, urn), json=payload)
    return (salt, handle_json_response(r))