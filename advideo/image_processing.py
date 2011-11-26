import hashlib

def calc_hash(value):
    h = hashlib.sha1()
    h.update(value)
    return h.hexdigest()
