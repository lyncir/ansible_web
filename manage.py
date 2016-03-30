# -*- coding: utf-8 -*-

from flask.ext.script import Manager, Server, prompt, \
        prompt_bool, prompt_pass

from app import app, db, bcrypt
from app.models import User

manager = Manager(app)


@manager.command
def createuser():
    '''Create super user for backend
    '''
    username = prompt("username", default='admin')
    password = prompt_pass('Password')
    confirm_password = prompt_pass('Retype Password')
    if password == confirm_password:
        user = User(username=username,
                    password=bcrypt.generate_password_hash(password),
                    active=1)
        db.session.add(user)
        db.session.commit()
    else:
        print "Sorry, passwords do not match."


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
