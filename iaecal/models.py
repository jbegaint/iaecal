# models.py

from iaecal import db


class Credentials(db.Model):
    __tablename__ = 'Credentials'

    session_id = db.Column(db.String(), primary_key=True, unique=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    key = db.Column(db.String())

    def __init__(self, session_id, key, username, password):
        self.session_id = session_id
        self.key = key
        self.username = username
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)
