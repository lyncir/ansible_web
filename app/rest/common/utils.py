# -*- coding: utf-8 -*-

from flask_restful import fields


class JsonItem(fields.Raw):
    def format(self, value):
        return json.loads(value)

