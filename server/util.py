from hashlib import sha3_256

def compute_commitment(salt, r, position):
    content = '{}{}{}'.format(salt, r, position)
    return sha3_256(content.encode('utf-8')).hexdigest()
