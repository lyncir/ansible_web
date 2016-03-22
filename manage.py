# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from app import app, db

manager = Manager(app)

@manager.command
def hello():
    print 'hello'


@manager.command
def init_db():
    print 'ready create database tables'
    db.create_all()
    print 'end create database tables'

if __name__ == '__main__':
    manager.run()
