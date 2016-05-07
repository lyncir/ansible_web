# -*- coding: utf-8 -*-

from . import app
from tasks import test


@app.route('/')
def index():
    #print test.delay()
    print test()
    return "ansible web"
