def index():
    return "Hello 4350api: no view, only JSON";

@request.restful()
def api():
    def GET(first_arg):
        if not first_arg == 'polls': raise HTTP(400)
        polls = db().select(db.polls.ALL).as_list()
        return dict(polls = polls)
    return locals();
