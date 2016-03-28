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


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(120))
    active = db.Column(db.Boolean())


    roles = db.relationship('Roles', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(100))


class Routes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(50))
    description = db.Column(db.String(100))


    roles = db.relationship('Roles', secondary=roles_routes,
                            backref=db.backref('routes', lazy='dynamic'))
