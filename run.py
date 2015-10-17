#!/usr/bin/env python2

import os
from iaecal import app

if __name__ == "__main__":
    print("=== Config ===")
    print("Setting: {}".format(os.environ['APP_SETTINGS']))
    print("Database url: {}".format(os.environ['DATABASE_URL']))
    app.run()
