import sys
import os

import urllib

# web2py imports

sys.path.append(os.path.abspath('/home/www-data/web2py/gluon'))

from contrib import simplejson

# unit test import

import unittest


class TestGetPolls(unittest.TestCase):
    
    def setUp(self):
        self.root = 'http://127.0.0.1:8274'
    
    def test_get_polls(self):
        
        response = urllib.urlopen(self.root + '/polls').read()
        
        responseJson = None
        try:
            responseJson = simplejson.loads(response)
        except simplejson.JSONDecodeError:
            self.fail("invalid response")

        self.assertEquals(type(responseJson), dict)

        self._test_polls_json_structure(responseJson)

    def _test_polls_json_structure(self, pollsJson):
        
        self.assertTrue('polls' in pollsJson)
        self.assertEquals(len(pollsJson), 1)
        
        polls = pollsJson['polls']
        self.assertEquals(type(polls), list)
        
        if len(polls) > 0:
            self._test_specific_poll_json_structure_in_polls(polls[0])
        
    def _test_specific_poll_json_structure_in_polls(self, pollJson):
        
        self.assertEquals(type(pollJson), dict)
        self.assertEquals(len(pollJson), 2)
        
        self.assertTrue('title' in pollJson)
        self.assertTrue('id' in pollJson)
