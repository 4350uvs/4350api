# Cross domain xhr request hack
#  When broswer sends a cross domain request, it will first sends a OPTIONS request.
#  For more detail in Please see the "Access-Control-Request-Method" section in
#  https://developer.mozilla.org/en-US/docs/HTTP/Access_control_CORS#The_HTTP_request_headers
if request.env.request_method == "OPTIONS":
    raise ok()