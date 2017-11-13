from Crypto.Hash import SHA3_256
from uuid import uuid4 as uuid

def random_r():
    '''
    Generates random r value
    '''
    return uuid().hex

def get_commitment_digest(r, position):
    '''
    Generates commitment, given r and position.
    Returns: (salt, digest)
    '''
    salt = uuid().hex
    plaintext = "{}{}{}".format(salt, r, position)
    return (salt, sha3_256(plaintext))

def sha3_256(text):
    '''Takes in string, return digest under SHA3-256'''
    sha3_obj = SHA3_256.new()
    sha3_obj.update(text.encode('utf-8'))

    return sha3_obj.hexdigest()
