import sys
import os

import urllib

sys.path.append(os.path.abspath('/home/www-data/web2py/gluon'))
from contrib import simplejson

from unittest import TestCase

class CommonTestCase(TestCase):
    
    def setUp(self):
        self.root = 'http://127.0.0.1:8274'
    
    def get(self, path):
        try:
            return urllib.urlopen(self.root + path).read()
        except Exeption:
            self.fail("can't open/read: " + self.root + path)
    
    def parseJson(self, s):
        try:
            jsonDict = simplejson.loads(s)
            self.assertEquals(type(jsonDict), dict)
            return jsonDict
        except simplejson.JSONDecodeError:
            self.fail("invalid response")