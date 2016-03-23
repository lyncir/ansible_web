# -*- coding: utf-8 -*-

from . import app
from .models import Hosts

@app.route('/')
def index():
    host = Hosts.query.get(1)
    return host.alias
