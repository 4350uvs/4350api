def index():
    return "Hello 4350api: no view, only JSON";

@request.restful()
def api():
    '''
       Documentation:
           https://github.com/4350uvs/4350api/wiki 
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
                choices = db(db.pollChoices.pid == pid).select(db.pollChoices.content)

                # we want to return a json array so we use Python's list
                choicesArray = []
                for choice in choices:
                    choicesArray.append(choice["content"])
    
                return dict(
                    poll = dict(
                        id = poll.id,
                        title = poll.title,
                        choices = choicesArray
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
        if not first_arg == 'polls':
            raise bad_request()

        if not check_params(['title', 'choice'], params):
            raise bad_request()

        # insert poll
        pid = db.polls.insert(title = params['title'])
        # insert poll choices
        choice_param = params['choice']
        if isinstance(choice_param, str):
            choice_param = [choice_param]
        for choice in choice_param:
            db.pollChoices.insert(pid = pid, content = choice)

        raise HTTP(201, pid, **{'Access-Control-Allow-Origin': '*', 'Content-Type': 'text/plain; charset=UTF-8'})

    return locals();
