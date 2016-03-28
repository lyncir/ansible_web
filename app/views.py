# -*- coding: utf-8 -*-

from . import app
from .models import Hosts
from .tasks import add

@app.route('/')
def index():
    result = add.delay(23, 42)
    host = Hosts.query.get(1)
    return host.alias
