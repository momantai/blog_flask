import hashlib

def encriptr(texto):
    enc = str.encode(texto)
    h = hashlib.sha1(enc)
    return h.hexdigest()
