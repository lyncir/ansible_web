# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with, fields
from flask_restful_swagger import swagger

from ... import db
from ...models import User


@swagger.model
class UserWithResourceFields:
    resource_fields = {
        "id": fields.Integer,
        "username": fields.String,
        "active": fields.Boolean
    }


class UserResource(Resource):
    "User Api"
    @swagger.operation(
        notes='get a user by id',
        responseClass=UserWithResourceFields.__name__,
        nickname='get',
        parameters=[
            {
                "name": "user_id",
                "description": "The id of the User",
                "required": True,
                "allowMultiple": False,
                "dataType": UserWithResourceFields.__name__,
                "paramType": "path"
            },
        ])
    @marshal_with(UserWithResourceFields.resource_fields)
    def get(self, user_id):
        user = User.query.get(user_id)
        return user

    def post(self):
        '''update'''
        pass

    def delete(self):
        '''delete'''
        pass


class UserCollectionResource(Resource):

    def get(self):
        '''query users'''
        pass

    def post(self):
        '''create user'''
        pass
