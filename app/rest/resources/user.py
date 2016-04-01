# -*- coding: utf-8 -*-

from flask_restful import Resource, marshal_with, fields
from flask_restful_swagger import swagger

from ... import db
from ...models import User


@swagger.model
class UserResourceFields:
    resource_fields = {
        "id": fields.Integer,
        "username": fields.String,
        "is_active": fields.Boolean
    }


class UserResource(Resource):
    "User Api"
    @swagger.operation(
        notes='Get the authenticated user',
    )
    @marshal_with(UserResourceFields.resource_fields)
    def get(self):
        user = User.query.get(1)
        return user

    @swagger.operation(
        notes="Update the authenticated user"
    )
    def patch(self):
        pass


class UsersResource(Resource):

    @swagger.operation(
        notes="Get all users"
    )
    def get(self):
        pass


class UserOtherResource(Resource):

    @swagger.operation(
        notes="Get a single user",
        nickname="get",
        parameters=[
            {
                "name": "username",
                "description": "Get a single user",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "path"
            },
        ]
    )
    @marshal_with(UserResourceFields.resource_fields)
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        return user
