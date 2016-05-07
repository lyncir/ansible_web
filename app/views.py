# -*- coding: utf-8 -*-

from . import app
from utils import get_inventory
from tasks import test


@app.route('/')
def index():
    #print test()
    get_inventory()
    return "ansible web"
