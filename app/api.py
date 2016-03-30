# -*- coding: utf-8 -*-

from flask.ext.restful import Resource
from flask_restful_swagger import swagger

from . import api


class Hosts(Resource):
    "Get hosts list"
    @swagger.operation(
        notes='get hosts list',
        responseClass='__name__',
        nicename='test',
        parameters=[
            {
                "name": "body",
                "description": "blueprint object that needs to be added. YAML",
                "required": True,
                "allowMultiple": False,
                "dataType": '__name__',
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "Created. The URL of the created blueprint should be in the Location header"
            },
            {
                "code": 405,
                "message": "Invalid input"
            }
        ]
    )

    def get(self):
        return {'hello': 'world'}


api.add_resource(Hosts, '/hosts')
