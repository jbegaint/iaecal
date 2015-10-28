#!/usr/bin/env python2

from flask.ext.assets import ManageAssets
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from iaecal import create_app, db
app = create_app()

from iaecal.models import *

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('assets', ManageAssets)


@manager.command
def resetdb():
    """
    Reset the database
    """
    db.drop_all()


if __name__ == '__main__':
    manager.run()
