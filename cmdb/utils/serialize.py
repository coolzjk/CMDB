#/usr/bin/env python
#-*- coding: utf-8 -*-
import json
from json import *
from lib.response import BaseResponse
class JsonEncoder(JSONEncoder):
    def default(self,field):
        if isinstance(field,BaseResponse):
            return field.__dict__

class Json(object):
    @staticmethod
    def dumps(response, ensure_ascii=True):
        return json.dumps(response,ensure_ascii=True,cls=JsonEncoder)
