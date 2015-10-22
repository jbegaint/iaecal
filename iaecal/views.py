# views.py

import datetime
from os import urandom
from flask import request, render_template, url_for, abort, jsonify
from cryptography.fernet import Fernet, InvalidToken
from flask_wtf.csrf import CsrfProtect
import wtforms_json

from iaecal import app, db, babel
from events import Calendar
from models import Credentials
from forms import UserInfoForm

SESSION_ID_LENGTH = 16

CsrfProtect(app)
wtforms_json.init()


def get_session_id():
    session_id = urandom(SESSION_ID_LENGTH).encode('hex')
    credentials = Credentials.query.filter_by(session_id=session_id).first()

    # In case a session with that id is already registered...
    if credentials is not None:
        # Try another session_id
        return get_session_id()
    return session_id


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


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['ACCEPT_LANGUAGES'])


@app.route("/", methods=['GET'])
def index():
    form = UserInfoForm()
    return render_template('index.html', form=form)


@app.route("/get-url", methods=['POST'])
def get_url():
    form = UserInfoForm.from_json(request.json)
    if form.validate():
        # Get the form data
        username = request.json['username']
        password = request.json['password']

        # Encode the data
        key = Fernet.generate_key()
        f = FernetCypher(key)
        username = f.encrypt(username)
        password = f.encrypt(password)

        session_id = get_session_id()
        key_part0, key_part1 = key[:len(key) / 2], key[len(key) / 2:]

        # Save the credentials
        credentials = Credentials(
            session_id=session_id,
            key=key_part0,
            username=username,
            password=password
        )
        db.session.add(credentials)
        db.session.commit()

        # Prepare the url to be returned
        key = key_part1.encode('hex')
        url = "{}?session_id={}&key={}".format(
            url_for('events', _external=True),
            session_id,
            key
        )
        return jsonify(url=url), 200
    return jsonify(errors=form.errors), 400


@app.route("/events/", methods=['GET'])
def events():
    session_id = request.args.get('session_id', None)
    key = request.args.get('key', None)

    if not session_id or not key:
        abort(404)

    credentials = Credentials.query.filter_by(session_id=session_id).first()

    # Try to decrypt the credentials for the session_id with the provided key
    try:
        key = "{}{}".format(credentials.key, key.decode('hex'))
        f = FernetCypher(key)
        username = f.decrypt(credentials.username)
        password = f.decrypt(credentials.password)
    except (TypeError, InvalidToken):
        abort(404)

    # Update stats
    credentials.last_used_on = datetime.datetime.utcnow()
    db.session.commit()

    # Get and parse the calendar data
    try:
        ics = Calendar(username, password).update().display()
    except ValueError:
        abort(404)
    return ics
