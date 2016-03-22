# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)

# flask-sqlalchemy
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'hello!'


# models
from models import Hosts
