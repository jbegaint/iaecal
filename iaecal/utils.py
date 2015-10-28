# iaecal/utils.py

import os
import requests
from cryptography.fernet import Fernet


def check_credentials(username, password):
    payload = {
        'username': username,
        'password': password
    }
    with requests.Session() as s:
        r = s.post(os.environ.get('CAL_LOGIN_URL'), data=payload)
        # Check redirect on success
        if r.history and r.history[0].status_code == 302:
            return True
    return False


class FernetCypher(object):
    def __init__(self, key):
        self.key = key

    def encrypt(self, secret):
        f = Fernet(self.key)
        if not isinstance(secret, bytes):
            secret = bytes(secret)
        return f.encrypt(secret)

    def decrypt(self, enc):
        f = Fernet(self.key)
        if not isinstance(enc, bytes):
            enc = bytes(enc)
        return f.decrypt(enc)
