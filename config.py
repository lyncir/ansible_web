# -*- coding: utf-8 -*-

import os


_basedir = os.path.abspath(os.path.dirname(__file__))

# Key
SECRET_KEY = os.urandom(24)

# Debug
DEBUG = False

# DB
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db'

del os
