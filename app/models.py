# -*- coding: utf-8 -*-

from . import db
from .users.models import *


class Host(db.Model):
    __tablename__ = 'hosts'

    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(20), unique=True)
    ip = db.Column(db.String(15))
    ip2 = db.Column(db.String(15))
    port = db.Column(db.Integer)
    remote_user = db.Column(db.String(20))

    def __init__(self, alias, ip, ip2, port, remote_user):
        self.alias = alias
        self.ip = ip
        self.ip2 = ip2
        self.port = port
        self.remote_user = remote_user

    def __repr__(self):
        return '<Host %r>' % self.alias
