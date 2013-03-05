from tests.common import CommonTestCase

class TestGetPoll(CommonTestCase):
    
    def setUp(self):
        self.post('/polls', {'title': 'unit test', 'choice': 'unit test'})
        
        self.responseJson = self.parseJson(self.get('/polls/1'))
    
    def test_poll_json_structure(self):
        
        # poll json
        pollJson = self.responseJson
        
        self.assertTrue('poll' in pollJson)
        self.assertEquals(len(pollJson), 1)
        
        # poll
        poll = pollJson['poll']
        self.assertEquals(type(poll), dict)
        
        self.assertTrue('id' in poll)
        self.assertEquals(type(poll['id']), int)
        
        self.assertTrue('title' in poll)
        self.assertEquals(type(poll['title']), unicode)
        
        self.assertTrue('choices' in poll)
        self.assertEquals(type(poll['choices']), list)
        
    def test_choices_in_poll(self):
        choices = self.responseJson['poll']['choices']
        
        if len(choices) < 1:
            return
        
        for choice in choices:
            
            self.assertEquals(type(choice), dict)
            self.assertEquals(len(choice), 2)

            self.assertTrue('id' in choice)
            self.assertEquals(type(choice['id']), int)
            
            self.assertTrue('content' in choice)
            self.assertEquals(type(choice['content']), unicode)
