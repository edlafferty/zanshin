import hashlib as hl
import json


def create_hash_256(string):
    """Create a SHA-256 hash of a string

    Arguments:
        :string: The string to hash
    """
    return hl.sha256(string).hexdigest()


def hash_block(block):
    """Hashes a block by adding '-' between the values

    Arguments:
        :block: The block to be hashed
    """
    return create_hash_256(json.dumps(block, sort_keys=True).encode())
    
    #hl.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
