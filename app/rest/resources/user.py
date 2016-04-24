# -*- coding: utf-8 -*-

from sqlalchemy import or_
from flask.ext.login import login_user, logout_user, login_required, \
        current_user
from flask_restful import Resource, marshal_with, fields, reqparse, abort
from flask_restful_swagger import swagger

from ... import db
from ...models import User


@swagger.model
class LoginResourceFields:
    resource_fields = {
        "access_token": fields.String,
    }


class LoginResource(Resource):
    "User login"
    @swagger.operation(
        notes="Login",
        nickname="post",
        parameters=[
            {
                "name": "username",
                "required": True,
                "dataType": "string",
                "paramType": "form",
            },
            {
                "name": "password",
                "required": True,
                "dataType": "string",
                "paramType": "form",
            },
            {
                "name": "remember",
                "required": False,
                "dataType": "boolean",
                "paramType": "form",
            }
        ]
    )
    @marshal_with(LoginResourceFields.resource_fields)
    def post(self):
        '''login'''
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('remember', type=str)
        args = parser.parse_args()
        user = User.query.filter_by(username=args['username'], active=1).first()
        if user and user.check_password(args['password']):
            if args['remember'] == 'true':
                login_user(user, remember=True)
            else:
                login_user(user)
            token = user.get_auth_token()
            return {'access_token': token.decode('ascii')}
        else:
            abort(409, message="Authorization failed.")


class LogoutResource(Resource):
    "User logout"
    @swagger.operation(
        notes="Logout",
        nickname="post"
    )
    @login_required
    def post(self):
        '''logout'''
        logout_user()
        return {'message': 'logout success.'}


@swagger.model
class UserResourceFields:
    resource_fields = {
        "id": fields.Integer,
        "username": fields.String,
        "email": fields.String,
        "active": fields.Boolean,
        "registered_on": fields.String
    }


class UserResource(Resource):
    "User Api"
    @swagger.operation(
        notes='Get the authenticated user',
    )
    @marshal_with(UserResourceFields.resource_fields)
    @login_required
    def get(self):
        return current_user

    @swagger.operation(
        notes="Sign up",
        nickname="post",
        parameters=[
            {
                "name": "username",
                "required": True,
                "dataType": "string",
                "paramType": "form"
            },
            {
                "name": "password",
                "required": True,
                "dataType": "string",
                "paramType": "form"
            },
            {
                "name": "email",
                "required": True,
                "dataType": "string",
                "paramType": "form"
            }
        ]
    )
    @marshal_with(UserResourceFields.resource_fields)
    def post(self):
        '''sign up'''
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()
        query = db.session.query(User).filter(or_(User.username==args['username'], \
                User.email==args['email'])).first()
        if query:
            abort(409, message="A user already exists.")
        user = User(username=args['username'], email=args['email'])
        user.generate_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return user

    @swagger.operation(
        notes="Update the authenticated user",
        nickname="patch",
        parameters=[
            {
                "name": "password",
                "required": True,
                "dataType": "string",
                "paramType": "form"
            }
        ]
    )
    @marshal_with(UserResourceFields.resource_fields)
    @login_required
    def patch(self):
        '''update password'''
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        current_user.generate_password(args['password'])
        db.session.commit()
        return current_user



class UsersResource(Resource):

    @swagger.operation(
        notes="Get all users"
    )
    @marshal_with(UserResourceFields.resource_fields)
    @login_required
    def get(self):
        return User.query.all()


class UserOtherResource(Resource):

    @swagger.operation(
        notes="Get a single user",
        nickname="get",
        parameters=[
            {
                "name": "username",
                "required": True,
                "dataType": 'string',
                "paramType": "path"
            },
        ]
    )
    @marshal_with(UserResourceFields.resource_fields)
    @login_required
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(409, message="User does not exists.")
        return user
