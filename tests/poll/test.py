from rapidsms.tests.harness import RapidTest
from textpoll import models as textpoll


class VoteCreateData(object):

    def create_poll(self, data={}):
    
    def create_option(self, data={}):
     
    def create_vote(self, data={}):



class VoteTest(VoteCreateData, RapidTest):


    def setUp(self):       

    def create_sample_poll(self):
        return poll

    def test_polls_closed(self):
        "User should recieve a message if there are no active polls."
   

    def test_vote(self):
        "Make sure voting is recorded properly with correct answers."

    def test_invalid_vote(self):
        "Only proper votes will get stored."


    def test_double_vote(self):
        "Double votes shouldn't cause any errors."
    

    def test_double_active_poll(self):
        "There should only ever be one active poll."
   
