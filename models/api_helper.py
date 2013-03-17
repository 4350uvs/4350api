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

# Note: Access-Control-xxx allows cross-domain ajax requests.
#       Google "Access_control_CORS" for more info.

headerThatAllowsCrossDomain = {
                                'Access-Control-Allow-Origin' : '*', 
                                'Access-Control-Allow-Methods': 'GET, POST, PUT, OPTIONS', 
                              }

def bad_request(response_body = ''):
    header = dict(headerThatAllowsCrossDomain.items() + {'Content-Type': 'text/plain; charset=UTF-8'}.items())
    return HTTP(400, response_body, **header)

def not_found(response_body = ''):
    header = dict(headerThatAllowsCrossDomain.items() + {'Content-Type': 'text/plain; charset=UTF-8'}.items())
    return HTTP(404, response_body, **header)

def created(response_body = ''):
    header = dict(headerThatAllowsCrossDomain.items() + {'Content-Type': 'text/plain; charset=UTF-8'}.items())
    return HTTP(201, response_body, **header)

def ok(response_body = ''):
    return HTTP(200, response_body, **headerThatAllowsCrossDomain)