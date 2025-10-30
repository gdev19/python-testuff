import os
import base64
def generate_id(length=20):
    id = base64.b16encode(os.urandom(length)).lower()
    id = id.decode("utf8")
    return id
