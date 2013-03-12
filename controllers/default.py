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
                choices = db(db.pollChoices.pid == pid).select(db.pollChoices.content, db.pollChoices.id)

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
                    db.pollChoices.insert(pid = pid, content = choice)

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
                pid = args[1]
                poll = db.polls[pid]
                if poll is not None:
                    cid = params['cid']
                    choice = db((db.pollChoices.pid == pid) & (db.pollChoices.id == cid)).select().first()
                    if choice is not None:
                        id = db.userChose.insert(cid = cid)
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