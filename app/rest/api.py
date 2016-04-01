# -*- coding: utf-8 -*-

from .. import api
from resources.user import UserResource, UsersResource, UserOtherResource


api.add_resource(UserResource, '/user')
api.add_resource(UsersResource, '/users')
api.add_resource(UserOtherResource, '/user/<string:username>')
