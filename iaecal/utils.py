# iaecal/utils.py

import os
import requests


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
