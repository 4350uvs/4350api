if not request.controller == 'appadmin':
    request.extension='json'

response.generic_patterns = ['*.json']
