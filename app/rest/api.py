# -*- coding: utf-8 -*-

from .. import api
from resources.user import LoginResource, LogoutResource, UserResource, \
        UsersResource, UserOtherResource
from resources.inventory import HostResource, HostOtherResource, \
        HostsResource


api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(UserResource, '/user')
api.add_resource(UsersResource, '/users')
api.add_resource(UserOtherResource, '/user/<string:username>')

api.add_resource(HostResource, '/host')
api.add_resource(HostOtherResource, '/host/<string:name>')
api.add_resource(HostsResource, '/hosts')
