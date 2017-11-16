from urllib.parse import urljoin

import logging
import requests

from utils import get_commitment_digest, calculate_commitment

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
        return None

def create_user():
    '''Creates a new user'''
    r = requests.post(urljoin(API_URL, 'users'))
    return handle_json_response(r)

def get_user(uid):
    '''Gets info regarding user'''
    urn = '/'.join(['users', str(uid)])
    r = requests.get(urljoin(API_URL, urn))

    return handle_json_response(r)

def get_users():
    '''Gets all users registered in PTC'''
    urn = '/users'
    r = requests.get(urljoin(API_URL, urn))

    return handle_json_response(r) or []

def create_game(uid, num_cups, num_players, rval, position):
    '''
    Creates a new cup shuffling game
    Returns: (salt, response)
    '''
    salt, digest = get_commitment_digest(rval, position)
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

def get_games():
    '''Gets all games registered in PTC'''
    urn = '/games'
    r = requests.get(urljoin(API_URL, urn))

    return handle_json_response(r)

def commit_game(gid, uid, gsalt, rval, guess):
    '''
    Bet on an ongoing cup shuffling game
    Returns: response
    '''
    commit = calculate_commitment(gsalt, rval, guess)
    urn = '/'.join(['games', str(gid), 'commit'])

    payload = {
        'user_id': uid,
        'commitment': commit
    }

    r = requests.post(urljoin(API_URL, urn), json=payload)
    return handle_json_response(r)

def reveal_position(gid, uid, rval, position):
    '''
    Reveals the correct position of the cup
    Returns: response from PTC
    '''
    urn = '/'.join(['games', str(gid), 'reveal'])
    payload = {
        'broker_id': uid,
        'r': rval,
        'position': position
    }

    r = requests.post(urljoin(API_URL, urn), json=payload)
    return handle_json_response(r)

def claim_winnings(gid, uid, rval):
    '''
    Claim winnings for particular user
    '''
    urn = '/'.join(['games', str(gid), 'claim'])
    payload = {
        'user_id': uid,
        'r': rval
    }

    r = requests.post(urljoin(API_URL, urn), json=payload)
    return handle_json_response(r)

def forfeit_game(gid):
    '''
    Forfeits the game
    '''
    urn = '/'.join(['games', str(gid), 'forfeit'])
    r = requests.post(urljoin(API_URL, urn))
    return handle_json_response(r)

def refund_deposit(gid):
    '''
    Broker gets deposit
    '''
    urn = '/'.join(['games', str(gid), 'refund_deposit'])
    r = requests.post(urljoin(API_URL, urn))
    return handle_json_response(r)

def advance_clock():
    '''
    Advances PTC clock
    '''
    urn = '/'.join(['clock', 'tick'])
    r = requests.post(urljoin(API_URL, urn))
    return handle_json_response(r)
