# -*- coding: utf-8 -*-

from . import db


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
    alias = db.Column(db.String(20), unique=True)
    ip = db.Column(db.String(15))
    ip2 = db.Column(db.String(15))
    port = db.Column(db.Integer)
    remote_user = db.Column(db.String(20))

    roles = db.relationship('Role', secondary=roles_hosts,
                            backref=db.backref('hosts', lazy='dynamic'))
    groups = db.relationship('Group', secondary=groups_hosts,
                            backref=db.backref('hosts', lazy='dynamic'))
