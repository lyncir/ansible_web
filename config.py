# -*- coding: utf-8 -*-

import os


_basedir = os.path.abspath(os.path.dirname(__file__))

# Key
SECRET_KEY = os.urandom(24)

# Debug
DEBUG = False

# DB
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# BROKER
CELERY_BROKER_URL = 'amqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'amqp://guest@locahost//'

# YML Template path
YML_TEMP_PATH = os.path.join(_basedir, 'app/yml_temp')

# Key dir
KEY_DIR = os.path.join(_basedir, 'app/keydir')

# Job password key
JOB_KEY = '\x93,\xf9\xfb\x1c@\x8f:*.\xc3\xe5\xaa3\xa3B\x1f\xf7\x8e\xcd\x14\xcer\x01'


del os
