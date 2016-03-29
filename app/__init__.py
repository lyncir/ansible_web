# -*- coding: utf-8 -*-

import re
import urlparse
from functools import wraps
from celery import Celery
from werkzeug.exceptions import Forbidden
from flask import Flask, g, render_template, redirect, url_for, session, \
        request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, login_user, \
        current_user, logout_user, login_required
from flask.ext.bcrypt import Bcrypt


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

login_manager.login_vieww = 'login'


@login_manager.user_loader
def load_user(user_id):
    from users.models import User

    return User.query.get(user_id)


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
        query1 = db.session.query(roles_users, roles_routes.c.route_id).join(roles_routes, roles_users.c.role_id==roles_routes.c.role_id).subquery()
        query2 = db.session.query(User, query1.c.role_id, query1.c.route_id).outerjoin(query1, User.id==query1.c.user_id).subquery()
        query3 = db.session.query(query2, Route.path).outerjoin(Route, query2.c.route_id==Route.id).filter(query2.c.username==current_user.username)
        re_strs = ','.join([i.path for i in query3])
        uri = unicode(request.url_rule)
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


# import all models, views
from models import *
from views import *
