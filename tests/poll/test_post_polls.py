from tests.common import CommonTestCase, HTTPCode

class TestPostPolls(CommonTestCase):
    
    def setUp(self):
        
        self.badQueryData  = [
                                {'title': 'xxx'},
                                {'choice': 'xxx'},
                             ]

        self.goodQueryData = [
                                {'title': '2 choices', 'choice': 'choice1', 'choice': 'choice2'},
                                {'title': '1 choices', 'choice': 'choice1'}
                             ]

    def _post(self, data):
        self.response = self.post('/polls', data)
        
    def test_reponse_code_bad_request(self):
        for data in self.badQueryData:
            self.assertEquals(type(data), dict)
            self._post(data)
            self.assertEquals(self.response['code'], HTTPCode.BAD_REQUEST)

    def test_reponse_code_created(self):
        for data in self.goodQueryData:
            self._post(data)
            self.assertEquals(self.response['code'], HTTPCode.CREATED)
            try:
                int(self.response['body'])
            except ValueError as e:
                self.fail('POST /poll returns non-integer. ' + str(e))