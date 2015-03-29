#!/usr/bin/env python2

import os
from events import Calendar

from flask import Flask, request
app = Flask(__name__)


def is_env_conf_valid():
    variables = ['CAL_LOGIN_URL', 'CAL_EVENTS_URL', 'CAL_USERNAME',
                 'CAL_PASSWORD']
    for v in variables:
        if os.environ.get(v) is None:
            return False
    return True


@app.route("/")
def hello():
    if not is_env_conf_valid():
        return "Invalid configuration"

    n = request.args.get('nWeeks')
    cal = Calendar(n)
    cal.update()

    return cal.display()


if __name__ == "__main__":
    DEBUG = bool(os.environ.get('FLASK_DEBUG', True))
    app.run(debug=DEBUG)
