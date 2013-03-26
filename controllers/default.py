import hashlib

def index():
    return "This is the 4350api. No view, only a JSON return.";

@request.restful()
def api():
    '''
       Documentation:
           https://github.com/4350uvs/4350api/wiki 

       the routes here is customized, please check 4350configurations repo on github.
    '''

    def GET(*args, **params):
        '''
            handles:
                1. GET /polls
                2. GET /polls/:pid
        '''

        if len(args) == 1 and args[0] == 'polls':
            # POST /polls
            polls = db().select(db.polls.ALL).as_list()
            return dict(polls = polls)
            
        elif len(args) == 2 and args[0] == 'polls' and args[1].isdigit():
            # GET /polls/:pid
            pid = args[1]
            poll = db.polls[pid]
            
            if poll is not None:
                choices = db(db.pollChoices.pid == pid).select(db.pollChoices.uvsContent, db.pollChoices.id)
                
                for choiceDict in choices:
                    # return "content" instead of "uvsContent"
                    choiceDict.content = choiceDict.uvsContent
                    # include chosenTimes
                    choiceDict.chosenTimes = db(db.userChose.cid == choiceDict.id).count()
                    
                    del choiceDict.uvsContent
                    
                return dict(
                    poll = dict(
                        id = poll.id,
                        title = poll.title,
                        choices = choices
                    )
                )
            else:
                raise not_found()

        else:
            raise not_found()
            
    def POST(first_arg, **params):
        '''
            handles:
                1. POST /polls
                2. POST /login
        '''

        if first_arg == 'polls':
            
            if check_params(['title', 'choice'], params):
                
                # insert poll
                pid = db.polls.insert(title = params['title'])
                
                # insert poll choices
                choice_param = params['choice']
                if isinstance(choice_param, str):
                    choice_param = [choice_param]
                for choice in choice_param:
                    db.pollChoices.insert(pid = pid, uvsContent = choice)
                    
                raise created(pid)

            else:
                raise bad_request()

        elif first_arg == 'login':

            if check_params(['username', 'password'], params):
                hash = hashlib.md5()
                hash.update(params['password'])
                hashPass = hash.digest()
                uNum = db((db.uvsUser.uvsUsername == params['username']) & (db.uvsUser.uvsPassword == hashPass)).count()
                
                if uNum == 1:
                    raise HTTP(200)

                else:
                    raise HTTP(550)

            else:
                raise bad_request()

        else:
            raise not_found()

    def PUT(*args, **params):
        '''
            handles:
                1. PUT /polls/:pid/choices
        '''

        if len(args) is 3 and args[0] == 'polls' and args[1].isdigit() and args[2] == 'choices':
            
            if check_params(['cid'], params):
                pid = args[1]
                poll = db.polls[pid]
                if poll is not None:
                    cid = params['cid']
                    choice = db((db.pollChoices.pid == pid) & (db.pollChoices.id == cid)).select().first()
                    if choice is not None:
                        id = db.userChose.insert(cid = cid)
                        if id is None:
                            raise bad_request()
                        raise ok()
                    else:
                        raise bad_request('bad cid')
                else:
                    raise bad_request('bad pid')
            else:
                raise bad_request('no cid in request body. ' + str(locals()))

        else:
            raise not_found()

    return locals();
