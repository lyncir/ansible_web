# -*- coding: utf8 -*-
from flask import render_template
from flask.ext.login import current_user

import users
from .. import app, permision


# Centralized URL
app.add_url_rule('/user/login', view_func=users.login, methods=['GET', 'POST'])
app.add_url_rule('/user/logout', view_func=users.logout)
app.add_url_rule('/user/add', view_func=users.adduser, methods=['GET', 'POST'])
app.add_url_rule('/user/<username>/profile', view_func=users.profile, methods=['GET', 'POST'])

@app.route('/')
@permision
def index():
    return render_template('index.html', current_user=current_user)
