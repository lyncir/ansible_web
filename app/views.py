# -*- coding: utf-8 -*-

from . import app
from .tasks import add

@app.route('/')
def index():
    task = add.delay(2, 3)
    return "ansible web %s" % task.id
