# -*- coding: utf-8 -*-

from . import app
from utils import get_inventory


@app.route('/')
def index():
    print get_inventory()
    return "ansible web"
