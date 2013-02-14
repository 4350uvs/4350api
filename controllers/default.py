def index():
    return "Hello 4350api: no view, only JSON";

@request.restful()
def api():

    def GET(first_arg):
        if not first_arg == 'polls': raise HTTP(400)
        polls = db().select(db.polls.ALL).as_list()
        return dict(polls = polls)

    def POST(first_arg, **params):
        if not first_arg == 'polls': raise HTTP(400)
        if not check_params(['title', 'choice'], params): raise HTTP(400)

        # insert poll
        pid = db.polls.insert(title = params['title'])
        # insert poll choices
        choice_param = params['choice']
        if isinstance(choice_param, str): choice_param = [choice_param]
        for choice in choice_param:
            db.pollChoices.insert(pid = pid, content = choice)

        raise HTTP(201, pid)

    return locals();
