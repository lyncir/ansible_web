# -*- coding: utf-8 -*-

import re
import urlparse
from functools import wraps
from celery import Celery
from werkzeug.exceptions import Forbidden
from flask import Flask, g, render_template, redirect, url_for, session, \
        request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, login_user, current_user, \
        logout_user, login_required
from flask.ext.bcrypt import Bcrypt


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)

# flask-sqlalchemy
db = SQLAlchemy(app)

# celery
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

celery = make_celery(app)

# flask bcrypt
bcrypt = Bcrypt(app)

# flask login
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_vieww = 'login'


class User(UserMixin):

    def __init__(self, query):
        self.id = query.id
        self.username = query.username
        self.password = query.password
        self.active = query.active

    def is_authenticated(self):
        return True

    def is_active(self):
        if self.active == 1:
            return True
        else:
            return False

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


@login_manager.user_loader
def load_user(user_id):
    user = Users.query.get(user_id)
    return User(user)


def uri_match(re_str, uri):
    '''match url
    :parm re_str: re string
    :parm uri: url
    '''
    if re.match(re_str, uri):
        return True
    else:
        return False


def permision(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        results = {'re_strs': '/*'}
        uri = unicode(request.url_rule)
        re_strs = results.get('re_strs')
        if re_strs:
            match = False
            for re_str in re_strs.split(','):
                match = uri_match(re_str, uri)
                if match:
                    break
            if match:
                return func(*args, **kwargs)
            else:
                raise Forbidden("You do not have access")
        else:
            raise Forbidden("You do not have access")
    return decorated_view


from models import *
from views import *
from forms import *
