# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from app import app, db

manager = Manager(app)

@manager.command
def hello():
    print 'hello'


@manager.command
def init_db():
    db.create_all()


@manager.command
def runserver():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    manager.run()
