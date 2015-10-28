# fabfile.py

from fabric.api import *
from base64 import b64encode
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


def deploy_setenv():
    """Set application settings on heroku."""
    # maintenance on
    local('heroku maintenance:on')

    # set environment variables
    config_dict = {
        'APP_SETTINGS': 'config.ProductionConfig',
        'SECRET_KEY': b64encode(os.urandom(24)),
        'CAL_EVENTS_URL': os.environ.get('CAL_EVENTS_URL'),
        'CAL_LOGIN_URL': os.environ.get('CAL_LOGIN_URL'),
        'MAIL_USERNAME': os.environ.get('MAIL_USERNAME'),
        'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD')
    }
    config = ' '.join(
        "%s=\"%s\"" % (k, v) for (k, v) in config_dict.iteritems()
    )

    local('heroku config:set %s' % config)

    # maintenance off
    local('heroku maintenance:off')


def deploy():
    """Deploy the application on heroku."""
    # maintenance on
    local('heroku maintenance:on')

    # push local changes
    local('git push heroku master')

    # run assets building
    local('heroku run python2 manage.py assets --parse-templates build')

    # upgrade database
    local('heroku run python2 manage.py db upgrade')

    # maintenance off
    local('heroku maintenance:off')
