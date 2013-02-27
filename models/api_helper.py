def check_params(required_list, incoming_params):
    '''
    return false if:
        1. incoming_params fails to contains any in required_list
        2. at least one in incoming_params is empty
    '''
    for param in required_list:
        if param not in incoming_params or len(incoming_params[param]) == 0:
            return False

    return True

def bad_request():
    return HTTP(400, **{'Access-Control-Allow-Origin': '*'})

def not_found():
    return HTTP(404, **{'Access-Control-Allow-Origin': '*'})
