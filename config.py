# config.py
import os


class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    # Babel
    ACCEPT_LANGUAGES = ['fr', 'en']
    BABEL_DEFAULT_LOCALE = 'fr'

    # Email
    MAIL_SERVER = "smtp.sendgrid.net"
    MAIL_PORT = 587
    MAIL_DEFAULT_SENDER = "server-error@iaecal.herokuapp.com"
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', None)
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', None)
    MAIL_ADMINS = ['jean.begaint@gmail.com']


class DevelopmentConfig(Config):
    DEBUG = True
