from tests.common import CommonTestCase

class TestGetPolls(CommonTestCase):
    
    def setUp(self):
        super(TestGetPolls, self).setUp()
        
        self.responseJson = self.parseJson(self.get('/polls'))
    
    def test_polls_json_structure(self):
        pollsJson = self.responseJson
        
        self.assertTrue('polls' in pollsJson)
        self.assertEquals(len(pollsJson), 1)
        
        polls = pollsJson['polls']
        self.assertEquals(type(polls), list)
        
    def test_poll_in_polls(self):
        polls = self.responseJson['polls']
        if len(polls) < 1:
            return
        
        for pollJson in polls:
        
            self.assertEquals(type(pollJson), dict)
            self.assertEquals(len(pollJson), 2)
            
            self.assertTrue('id' in pollJson)
            self.assertEquals(type(pollJson['id']), int)
            
            self.assertTrue('title' in pollJson)
            self.assertEquals(type(pollJson['title']), unicode)
