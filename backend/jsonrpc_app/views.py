from django.shortcuts import render
from rest_framework.views import APIView
from simplejson import loads, dumps
from django.http import HttpResponse
import traceback, sys

class HttpResponseForbidden(HttpResponse):
    status_code = 403

class HttpResponseError(HttpResponse):
    status_code = 500

# Create your views here.
class JsonRpcApp(APIView):
    def post(self, req):
        try:
            json = loads(req.body)
        except ValueError as e:
            raise ValueError('Bad JSON: %s' % e)
        try:
            method = json['method']
            params = json['params']
            id = json['id']
        except KeyError as e:
            raise ValueError("JSON body missing parameter: %s" % e)

        if method.startswith('_'):
            raise HttpResponseForbidden("Bad method name %s: must not start with _" % method)

        if not isinstance(params, list):
            raise ValueError("Bad params %r: must be a list" % params)

        try:
            method = getattr(self, method)
        except AttributeError:
            raise ValueError("No such method %s" % method)
        
        try:
            result = method(*params)
        except:
            text = traceback.format_exc()
            exc_value = sys.exc_info()[1]
            error_value = dict(name = 'JSONRPCError', code = 100, message=str(exc_value), error=text)
            return HttpResponseError(dumps(dict(result=None, error=error_value, id=id)))
        
        resp = HttpResponse(dumps(dict(result = result,error = None,id = id)))
        return resp

    def addnumbers(self, a, b):
        return a+b