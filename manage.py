# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from app import app, db, bcrypt
from app.users.models import Users, Roles, Routes

manager = Manager(app)

@manager.command
def createsuperuser():
    password = bcrypt.generate_password_hash('123456')
    role = Roles(name='administrators')
    user = Users(username='admin', password=password, active=1)
    route = Routes(path='/*')
    role.users.append(user)
    role.routes.append(route)
    db.session.add(role)
    db.session.commit()


@manager.command
def init_db():
    db.create_all()


@manager.command
def runserver():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    manager.run()
