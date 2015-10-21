# fabfile.py

from fabric.api import *


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
