#!/usr/bin/env python2

import os
from iaecal import create_app

print("=== Config ===")
print("Setting: {}".format(os.environ['APP_SETTINGS']))
print("Database url: {}".format(os.environ['DATABASE_URL']))
app = create_app()

if __name__ == "__main__":
    app.run()
