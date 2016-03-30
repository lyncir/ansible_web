# -*- coding: utf-8 -*-

from .. import api
from resources.user import UserResource, UserCollectionResource


api.add_resource(UserResource, '/user/<string:user_id>')
api.add_resource(UserCollectionResource, '/users')
