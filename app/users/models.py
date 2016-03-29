# -*- coding: utf-8 -*-

from .. import db


roles_users = db.Table(
    'roles_users',
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')),
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')))


roles_routes = db.Table(
    'roles_routes',
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')),
    db.Column('route_id', db.Integer(), db.ForeignKey('routes.id')))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(120))
    active = db.Column(db.Boolean())


    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_active(self):
        """True, as all users are active."""
        return self.active

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return unicode(self.id)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(100))


class Route(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(50))
    description = db.Column(db.String(100))


    roles = db.relationship('Role', secondary=roles_routes,
                            backref=db.backref('routes', lazy='dynamic'))
