from tests.common import CommonTestCase, HTTPCode

class TestPostPolls(CommonTestCase):
    
    def setUp(self):
        
        self.badQueryData  = [
                              # some are commented because urllib2
                              # doesn't support non-dict query string
#                               {''}, 
                                {'xxx': 'xxx'},
                                {'id': 'xxx'},
#                               {'cid'}
                             ]
        
        self.pid = self.post('/polls', {'title': '1 choices', 'choice': 'choice1'})['body']
        newestPoll = self.parseJson(self.get('/polls/' + self.pid))
        self.cid = newestPoll['poll']['choices'][0]['id']
    
    def _put(self, pid, data):
        path = '/polls/{0}/choices'.format(pid)
        return self.put(path, data)
    
    def test_reponse_code_bad_request(self):
        # bad params
        for data in self.badQueryData:
            response = self._put(self.pid, data)
            self.assertEquals(response['code'], HTTPCode.BAD_REQUEST)
        
        # bad pid
        newestPid = self.pid
        notExistedPid = str(int(newestPid) + 1)
        response = self._put(notExistedPid, {'cid': self.cid})
        self.assertEquals(response['code'], HTTPCode.NOT_FOUND)

        # bad cid
        newestCid = self.cid
        notExistedcid = str(int(newestCid) + 1)
        response = self._put(self.pid, {'cid': notExistedcid})
        self.assertEquals(response['code'], HTTPCode.BAD_REQUEST)
        
    def test_reponse_code_ok(self):
        response = self._put(self.pid, {'cid': self.cid})
        self.assertEquals(response['code'], HTTPCode.OK)
