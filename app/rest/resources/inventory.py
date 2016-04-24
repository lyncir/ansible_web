# -*- coding: utf-8 -*-

from flask.ext.login import login_required
from flask_restful import Resource, marshal_with, fields, reqparse, abort
from flask_restful_swagger import swagger

from ... import db
from ...models import Host, Group


class HostResourceFields:
    resource_fields = {
        "id": fields.Integer,
        "name": fields.String,
        "host": fields.String,
        "port": fields.Integer,
        "user": fields.String
    }


class HostResource(Resource):
    "Host api"
    
    @swagger.operation(
        notes="add a host",
        nickname="post",
        parameters=[
            {
                "name": "name",
                "required": True,
                "dataType": "string",
                "paramType": "form"
            },
            {
                "name": "host",
                "description": "ansible_host",
                "required": True,
                "dataType": "string",
                "paramType": "form"
            },
            {
                "name": "port",
                "description": "ansible_port",
                "required": True,
                "dataType": "int",
                "paramType": "form"
            },
            {
                "name": "user",
                "description": "ansible_user",
                "required": True,
                "dataType": "string",
                "paramType": "form"
            }
        ]
    )
    @marshal_with(HostResourceFields.resource_fields)
    @login_required
    def post(self):
        "add a host"
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('host', type=str)
        parser.add_argument('port', type=int)
        parser.add_argument('user', type=str)
        args = parser.parse_args()
        query = Host.query.filter_by(name=args['name']).first()
        if query:
            abort(409, message="Host already exists.")

        host = Host(name=args['name'], 
                    host=args['host'], 
                    port=args['port'], 
                    user=args['user'])
        db.session.add(host)
        db.session.commit()
        return host


class HostOtherResource(Resource):

    @swagger.operation(
        notes="Get a host info by name",
        nickname="get",
        parameters=[
            {
                "name": "name",
                "required": True,
                "dataType": "string",
                "paramType": "path"
            }    
        ]
    )
    @marshal_with(HostResourceFields.resource_fields)
    @login_required
    def get(self, name):
        "get a host by name"
        host = Host.query.filter_by(name=name).first()
        if not host:
            abort(409, message="host does not exists")
        return host

    def patch(self, name):
        "update a host by name"
        pass

    def delete(self, name):
        "delete a host by name"
        pass
    

class HostsResource(Resource):
    "Hosts api"

    def get(self):
        "Get all host info"
        pass

