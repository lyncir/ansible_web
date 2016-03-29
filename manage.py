# -*- coding: utf-8 -*-

from flask.ext.script import Manager, Server, prompt, \
        prompt_bool, prompt_pass

from app import app, db, bcrypt
from app.users.models import User, Role, Route

manager = Manager(app)


@manager.command
def createsuperuser():
    '''Create super user for backend
    '''
    username = prompt("username", default='admin')
    password = prompt_pass('Password')
    role = Role(name='administrators')
    user = User(username=username,
                password=bcrypt.generate_password_hash(password),
                active=1)
    route = Route(path='/*')
    role.users.append(user)
    role.routes.append(route)
    db.session.add(role)
    db.session.commit()


@manager.command
def initdb():
    '''Craete SQL tables
    '''
    db.create_all()


@manager.command
def dropdb():
    '''Drop tables if you sure
    '''
    if prompt_bool(
        "Are you sure you want to lose all your data"):
        db.drop_all()


# Defalut commands
manager.add_command('runserver', Server())

if __name__ == '__main__':
    manager.run()
