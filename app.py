#!/usr/bin/env python2

import os
from events import Calendar

from flask import Flask, request
app = Flask(__name__)

ENV_VARS = [
    'CAL_EVENTS_URL',
    'CAL_LOGIN_URL',
    'CAL_PASSWORD',
    'CAL_USERNAME',
]
N_WEEKS = 4


def is_env_conf_valid():
    for v in ENV_VARS:
        if os.environ.get(v) is None:
            return False
    return True


@app.route("/")
def hello():
    if not is_env_conf_valid():
        return "Invalid configuration"

    n = request.args.get('nWeeks', N_WEEKS)
    cal = Calendar(n)
    cal.update()

    return cal.display()


if __name__ == "__main__":
    DEBUG = bool(os.environ.get('FLASK_DEBUG', False))
    app.run(debug=DEBUG)
