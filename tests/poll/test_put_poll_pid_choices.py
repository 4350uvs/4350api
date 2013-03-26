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
        self.currChosenTimes = newestPoll['poll']['choices'][0]['chosenTimes']
    
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
        self.assertEquals(response['code'], HTTPCode.BAD_REQUEST)

        # bad cid
        newestCid = self.cid
        notExistedcid = str(int(newestCid) + 1)
        response = self._put(self.pid, {'cid': notExistedcid})
        self.assertEquals(response['code'], HTTPCode.BAD_REQUEST)
        
    def test_reponse_code_ok(self):
        # choseTimes is zero before PUT request
        self.assertEquals(self.currChosenTimes, 0)
        
        response = self._put(self.pid, {'cid': self.cid})
        self.assertEquals(response['code'], HTTPCode.OK)
        
        self._test_chosen_times_increased
        
        response = self._put(self.pid, {'cid': self.cid})
        self.assertEquals(response['code'], HTTPCode.OK)
        
        self._test_chosen_times_increased
    
    def _test_chosen_times_increased(self):
        testPoll = self.parseJson(self.get('/polls/' + self.pid))
        chosenTimes = testPoll['poll']['choices'][0]['chosenTimes']
        self.assertEquals(chosenTimes, self.currChosenTimes + 1)
        