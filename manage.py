#!/usr/bin/env python2

import os

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from iaecal import app, db
app.config.from_object(os.environ['APP_SETTINGS'])

from iaecal.models import *

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def resetdb():
    """Drop all the tables in the database."""
    db.drop_all()

if __name__ == '__main__':
    manager.run()
