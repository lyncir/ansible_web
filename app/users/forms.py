# -*- coding: utf8 -*-

from urlparse import urlparse, urljoin
from flask import g, request, redirect, url_for
from flask.ext.wtf import Form
from flask.ext.login import current_user
from wtforms import fields, validators

from .. import bcrypt
from ..users.models import Users


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
            ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


class RedirectForm(Form):
    next = fields.HiddenField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or '/'

    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


class LoginForm(RedirectForm):
    username = fields.StringField(u'Username', validators=[validators.DataRequired()])
    password = fields.PasswordField(u'Password',
            validators=[validators.DataRequired()])

    def validate_username(self, field):
        user = self.get_user()
        if user:
            #if self.password.data != user.password:
            if not bcrypt.check_password_hash(user.password, self.password.data):
                raise validators.ValidationError("Username or Password Error!")
        else:
            raise validators.ValidationError("Username or Password Error!")

    def get_user(self):
        user = Users.query.filter_by(username=self.username.data, active=1).first()
        return user


class AddUserForm(Form):
    username = fields.StringField(u'Username', validators=[validators.DataRequired()])
    password = fields.PasswordField(u'Password',
            validators=[validators.DataRequired()])

    def validate_username(self, field):
        user = Users.query.filter_by(username=self.username.data).first()
        if user:
            raise validators.ValidationError('User is exists')


class ChangedPasswordForm(Form):
    username = fields.StringField(u'Username', validators=[validators.DataRequired()])
    old_password = fields.PasswordField(u'Old Password', validators=[validators.DataRequired()])
    new_password = fields.PasswordField(u'New Password',
            validators=[validators.DataRequired(),
                        validators.EqualTo('confirm_password', message='Password must be match')])
    confirm_password = fields.PasswordField(u'Confirm Password', validators=[validators.DataRequired()])

    def validate_old_password(self, field):
        oldpassword = current_user.password
        #if self.old_password.data != oldpassword:
        if not bcrypt.check_password_hash(oldpassword, self.old_password.data):
            raise validators.ValidationError("Password must be match")
