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
            polls = db(db.uvsSession.uvsType == 'poll').select(db.uvsSession.ALL).as_list()
            return dict(polls = polls)

        elif len(args) == 2 and args[0] == 'polls' and args[1].isdigit():
            # GET /polls/:pid
            pid = args[1]
            poll = db.Session[pid]

            if poll is not None and poll.type == 'poll':
                q = db(db.Question.sessionID == pid).select(db.Question.ALL)
                choices = db(db.MultipleChoice.questionID == q.id).select(db.MultipleChoice.choiceText, db.MultipleChoice.id)

                return dict(
                    poll = dict(
                        id = Session.id,
                        title = Session.name,
                        question = q.questionText,
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
        '''
        if first_arg == 'polls':

            if check_params(['title', 'question', 'choice'], params):

                # insert poll
                sid = db.Session.insert(name = params['title'], type = 'poll')
                
                # insert question
                qid = db.Question.insert(sessionID = sid, questionText = params['question'], code = 'MC')

                # insert poll choices
                choice_param = params['choice']
                if isinstance(choice_param, str):
                    choice_param = [choice_param]
                for choice in choice_param:
                    db.MultipleChoice.insert(questionID = qid, text = choice, correct = False)

                raise HTTP(201, pid, **{'Access-Control-Allow-Origin': '*', 'Content-Type': 'text/plain; charset=UTF-8'})

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
                sid = args[1]
                poll = db.Session[sid]
                if poll is not None and poll.type == 'poll':
                    cid = params['cid']
                    qid = db(db.Question.sessionID == sid).select(db.Question.id)
                    choice = db((db.MultipleChoice.questionID == qid) & (db.MultipleChoice.id == cid)).select().first()
                    if choice is not None:
                        saID = db.SessionAnswer.insert(sessionID = sid)
                        id = db.Answer.insert(sessionAnswerID = saID, questionID = qid, answerText = cid)
                        if id is None:
                            raise bad_request()
                    else:
                        raise bad_request()
                else:
                    raise not_found()
            else:
                raise bad_request()
        else:
            raise not_found()

    return locals();
