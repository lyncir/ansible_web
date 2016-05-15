# -*- coding: utf-8 -*-

import json
from flask.ext.login import login_required
from flask_restful import Resource, marshal_with, fields, reqparse, abort
from flask_restful_swagger import swagger

from ... import db
from ...models import Job
from ...rest.common.utils import JsonItem


class JobResourceFields:
    resource_fields = {
        "id": fields.Integer,
        "job_id": fields.String,
        "playbooks": JsonItem,
        "run_data": JsonItem,
        "private_key_file": fields.String,
        "password": fields.String,
        "verbosity": fields.String,
        "stats": fields.String,
        "started": fields.DateTime(dt_format='rfc822'),
        "finished": fields.DateTime(dt_format='rfc822')
    }


class JobResource(Resource):
    '''Job api'''

    @swagger.operation(
        notes="add a job",
        nickname="post",
        parameters=[
            {
                "name": "job_id",
                "required": True,
                "dataType": "string",
                "paramType": "form"
            }, 
            {
                "name": "playbooks",
                "required": True,
                "dataType": "multi",
                "paramType": "form"
            }, 
            {
                "name": "run_data",
                "required": True,
                "dataType": "string",
                "paramType": "form"
            }, 
            {
                "name": "private_key_file",
                "required": False,
                "dataType": "string",
                "paramType": "form"
            }, 
            {
                "name": "password",
                "required": False,
                "dataType": "string",
                "paramType": "form"
            }, 
            {
                "name": "verbosity",
                "required": False,
                "dataType": "int",
                "paramType": "form"
            }, 
        ]
    )
    @marshal_with(JobResourceFields.resource_fields)
    def post(self):
        '''add a job'''
        parser = reqparse.RequestParser()
        parser.add_argument('job_id', type=str, required=True)
        parser.add_argument('playbooks', action='append', required=True)
        parser.add_argument('run_data', type=json.loads, required=True)
        parser.add_argument('private_key_file', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('verbosity', type=int)
        args = parser.parse_args()
        query = Job.query.filter_by(job_id=args['job_id']).first()
        if query:
            abort(409, message="Job already exists.")

        job = Job(job_id=args['job_id'],
                  playbooks=json.dumps(args['playbooks']),
                  run_data=json.dumps(args['run_data']),
                  private_key_file=args['private_key_file'],
                  password=args['password'],
                  verbosity=args['verbosity'])
        db.session.add(job)
        db.session.commit()
        return job
    

class JobOtherResource(Resource):

    @swagger.operation(
        notes="get a job status by id",
        nickname="get",
    )
    def get(self, id):
        '''get a job status by id'''
        pass

    @swagger.operation(
        notes="update job by id",
        nickname="patch",
    )
    def patch(self, id):
        '''update job by id'''
        pass
    
    @swagger.operation(
        notes="delete job by id",
        nickname="delete",
    )
    def delete(self, id):
        '''delete job by id'''
        pass


class JobsResource(Resource):
    '''jobs api'''

    @swagger.operation(
        notes="list all jobs status",
        nickname="get",
    )
    @marshal_with(JobResourceFields.resource_fields)
    def get(self):
        '''list all jobs status'''
        jobs = Job.query.all()
        return jobs
