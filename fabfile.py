# fabfile.py

from fabric.api import *
import os


def initbabel():
    """Init babel."""
    # Extract strings to translate
    local('pybabel extract -F babel.cfg -o messages.pot iaecal')
    # Add languages translations
    local('pybabel init -i messages.pot -d iaecal/translations -l en')
    local('pybabel init -i messages.pot -d iaecal/translations -l fr')


def babel():
    """Compile translations."""
    # Extract strings to translate
    local('pybabel extract -F babel.cfg -o messages.pot iaecal')
    # Add languages translations
    local('pybabel update -i messages.pot -d iaecal/translations -l en')
    local('pybabel update -i messages.pot -d iaecal/translations -l fr')
    # Compile the translations
    local('pybabel compile -d iaecal/translations')


def test():
    """Test the application."""
    local('python2 iaecal_tests.py')


def deploy():
    """Deploy the application on heroku."""
    # maintenance on
    local('heroku maintenance on')

    # push local changes
    local('git push heroku master')

    # set environment variables
    local('heroku config:set APP_SETTINGS:config.ProductionConfig')

    secret_key = os.urandom(24)
    local('heroku config:set SECRET_KEY:%s' % secret_key)

    env_vars = ['CAL_EVENTS_URL', 'CAL_LOGIN_URL', 'MAIL_USERNAME',
                'MAIL_PASSWORD']
    for v in env_vars:
        local('heroku config:set %s:%s' % (v, os.environ.get(v)))

    # maintenance off
    local('heroku maintenance off')
