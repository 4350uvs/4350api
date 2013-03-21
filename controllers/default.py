def index():
    return "This is the 4350api. No view, only a JSON return.";

def user():
    return dict(form=auth())

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
                3. GET /lectures/:sid
                4. GET /lectures/:username
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
                
        elif len(args) == 2 and args[0] == 'lectures' and args[2].isdigit():
            # GET /lectures/:sid
            sid = args[1]
            ses = db.uvsSession[sid]
            
            if ses is not None and ses.uvsType == 'lecture':
                questions = db(db.Question.sessionID == sid).select(db.Question.ALL)
                
                if questions is not None:
                    return dict(
                        ses = dict(
                            id = ses.id,
                            title = ses.name,
                            startDate = ses.startDate,
                            questions = questions
                        )
                    )
                else:
                    raise not_found()
                    
            else:
                raise not_found()
                
        elif len(args) == 2 and args[0] == 'lectures':
             # GET /lectures/:username
             uid = db(db.uvsUser.username == args[1]).select(db.uvsUser.id)
             uid = uid[0]
             groups = db((db.Membership.userID == uid) & (db.uvsGroup.id == db.Membership.id)).select(db.uvsGroup.ALL)
             lects = db((groups.id == db.uvsSession.sessionOwner) & (db.uvsSession.uvsType == 'lecture')).select(db.uvsSession.ALL)
             
             return dict(lects = lects)
             
        else:
            raise not_found()
            
    def POST(first_arg, **params):
        '''
            handles:
                1. POST /polls
                2. POST /lectures
                3. POST /lectures/question
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

        elif len(args) == 1 and first_arg == 'lectures':
            if check_params(['title', 'date', 'groupname'], params):
                
                grp = db(db.uvsGroup.name == params['groupname']).select(db.uvsGroup.ALL)

                if grp is not None:
                    gid = grp[0].id
                    # insert lectue
                    sid = db.uvsSession.insert(name = params['title'], sessionOwner = gid, uvsType = 'lecture', startDate = params['date'])

                    raise created(sid)

                else: 
                    raise not_found()
            else:
                raise bad_request()

        elif len(args) == 2 and args[0] == 'lectures':
            if check_params(['session', 'text', 'choice'], params):
                correctAnswer = True
                # insert question (multiple choice)
                qid = db.Question.insert(sessionID = params['session'], questionText = params['text'], code = 'MC')

                # insert choices
                choice_param = params['choice']
                if isinstance(choice_param, str):
                    choice_param = [choice_param]
                for choice in choice_param:
                    db.MultipleChoice.insert(questionID = qid, choiceText = choice, correct = correctAnswer)
                    # only the first answer is 'correct', make all others false
                    correctAnswer = False

                raise created(qid)

            elif check_params(['session', 'title'], params):
                # insert question (long answer)
                qid = db.Question.insert(sessionID = params['session'], questionText = params['text'], code = 'LA')

                raise created(qid)

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
