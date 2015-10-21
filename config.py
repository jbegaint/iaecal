# config.py
import os


class Config(object):
    BABEL_DEFAULT_LOCALE = 'fr'
    ACCEPT_LANGUAGES = ['fr', 'en']
    DEBUG = False
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class DevelopmentConfig(Config):
    DEBUG = True
