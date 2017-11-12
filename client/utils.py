import random

from Crypto.Hash import SHA3_256

def randhex(size=1):
    '''
    Generates a random hexadecimal sequence of size length
    Returns: random hexadecimal string
    '''
    result = []
    for i in range(size):
        result.append(str(random.choice("0123456789abcdef")))
    return "".join(result)

def get_commitment_digest(r, position):
    '''
    Generates commitment, given r and position.
    Returns: (salt, digest)
    '''
    salt = randhex(32)
    plaintext = "{}{}{}".format(salt, r, position)
    return (salt, sha3_256(plaintext))

def sha3_256(text):
    '''Takes in string, return digest under SHA3-256'''
    sha3_obj = SHA3_256.new()
    sha3_obj.update(text.encode('utf-8'))

    return sha3_obj.hexdigest()
