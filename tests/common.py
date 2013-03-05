import sys
import os

import urllib, urllib2

sys.path.append(os.path.abspath('/home/www-data/web2py/gluon'))
from contrib import simplejson

from unittest import TestCase

class CommonTestCase(TestCase):
    
    ROOT = 'http://127.0.0.1:8274'

    USER_AGENT = 'unittest'

    def _open(self, path, data = None, method = None):
        if type(data) == dict or type(data) == set:
            data = urllib.urlencode(data)

        request = urllib2.Request(CommonTestCase.ROOT + path)
        request.add_header('User-Agent', CommonTestCase.USER_AGENT)
        
        # set http request method
        #    GET is the default
        #    POST if data is specified but method is specified
        #    Other if data and method is specified
        if method is not None:
            request.get_method = lambda: method
        
        try:
            opener = urllib2.urlopen(request, data)
            return {'code': opener.getcode(), 'body': opener.read()}
        except urllib2.HTTPError as e:
            return {'code': e.code, 'body': e.read()}
    
    def get(self, path):
        return self._open(path)['body']
    
    def post(self, path, data):
        return self._open(path, data)

    def put(self, path, data):
        method = lambda: 'PUT'
        return self._open(path, data, 'PUT')
    
    def parseJson(self, s):
        try:
            jsonDict = simplejson.loads(s)
            self.assertEquals(type(jsonDict), dict)
            return jsonDict
        except simplejson.JSONDecodeError:
            self.fail("invalid response")

class HTTPCode:
    BAD_REQUEST = 400
    CREATED = 201
    OK = 200
    NOT_FOUND = 404
