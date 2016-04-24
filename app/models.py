# -*- coding: utf-8 -*-
from datetime import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer 
                          as Serializer, BadSignature, SignatureExpired)

from . import app, db, bcrypt


roles_users = db.Table(
    'roles_users',
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')),
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')))


roles_groups = db.Table(
    'roles_groups',
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')),
    db.Column('group_id', db.Integer(), db.ForeignKey('groups.id')))


roles_hosts = db.Table(
    'roles_hosts',
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')),
    db.Column('host_id', db.Integer(), db.ForeignKey('hosts.id')))


groups_hosts = db.Table(
    'groups_hosts',
    db.Column('group_id', db.Integer(), db.ForeignKey('groups.id')),
    db.Column('host_id', db.Integer(), db.ForeignKey('hosts.id')))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(50), unique=True, index=True)
    active = db.Column(db.Boolean(), default=1)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow())

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def generate_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def get_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def check_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User %r>' % (self.username)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(100))


class Group(db.Model):
    '''About server'''
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(100))

    roles = db.relationship('Role', secondary=roles_groups,
                            backref=db.backref('groups', lazy='dynamic'))

class Host(db.Model):
    '''About server'''
    __tablename__ = 'hosts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, index=True)
    host = db.Column(db.String(15))
    port = db.Column(db.Integer)
    user = db.Column(db.String(20))

    roles = db.relationship('Role', secondary=roles_hosts,
                            backref=db.backref('hosts', lazy='dynamic'))
    groups = db.relationship('Group', secondary=groups_hosts,
                            backref=db.backref('hosts', lazy='dynamic'))

    def __repr__(self):
        return '<Host %r>' % (self.name)
