import sys
import os

import urllib, urllib2

sys.path.append(os.path.abspath('/home/www-data/web2py/gluon'))
from contrib import simplejson

from unittest import TestCase

class CommonTestCase(TestCase):
    
    ROOT = 'http://127.0.0.1:8274'

    USER_AGENT = 'unittest'

    def _open(self, path, data = None):
        if type(data) == dict:
            data = urllib.urlencode(data)

        request = urllib2.Request(CommonTestCase.ROOT + path)
        request.add_header('User-Agent', CommonTestCase.USER_AGENT)
        
        return urllib2.urlopen(request, data)
    
    def get(self, path):
        return self._open(path).read()
    
    def post(self, path, data):
        try:
            opened = self._open(path, data)
            return {'code': opened.getcode(), 'body': opened.read()}
        except urllib2.HTTPError as e:
            return {'code': e.code, 'body': e.read()}

    
    def parseJson(self, s):
        try:
            jsonDict = simplejson.loads(s)
            self.assertEquals(type(jsonDict), dict)
            return jsonDict
        except simplejson.JSONDecodeError:
            self.fail("invalid response")
