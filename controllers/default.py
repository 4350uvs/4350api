def index():
    return "Hello 4350api: no view, only JSON";

@request.restful()
def api():

    def GET(*args, **params):
        if len(args) == 0 or args[0] != 'polls':
            raise bad_request()

        if len(args) == 1:
            # all polls
            polls = db().select(db.polls.ALL).as_list()
            return dict(polls = polls)
        elif len(args) == 2 and args[1].isdigit():
            # specific poll
            pid = args[1]
            poll = db.polls[pid]

            if poll is not None:
                # TODO query all poll options
                return dict(poll = poll)
            else:
                raise not_found();
        else:
            return locals();

    def POST(first_arg, **params):
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
