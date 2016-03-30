# -*- coding: utf-8 -*-

from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.restful import Api
from flask_restful_swagger import swagger


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)

# flask-sqlalchemy
db = SQLAlchemy(app)


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

# celery
celery = make_celery(app)

# flask bcrypt
bcrypt = Bcrypt(app)

# flask login
login_manager = LoginManager()
login_manager.init_app(app)

# flask rest api
api = swagger.docs(Api(app), apiVersion='0.1')


@login_manager.user_loader
def load_user(user_id):
    from models import User

    return User.query.get(user_id)


# import all models, views, api
from models import *
from views import *
from rest.api import *
