# handle 403 error
from django.shortcuts import render, render_to_response
from django.template import RequestContext


# handle 403 error
def handler403(request, exception):
    context = {
        "message": exception,
    }
    response = render_to_response('403.html', context)
    response.status_code = 403
    return response