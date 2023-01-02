# handle 403 error
from django.http import JsonResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from chat.models import Room
from django.contrib.auth import get_user_model

User = get_user_model()
# handle 403 error
def handler403(request, exception):
    context = {
        "message": exception,
    }
    response = render_to_response('403.html', context)
    response.status_code = 403
    return response
def test(request):
    # return render(request, 'test.html', {})
    room = Room()
    room.name = 'test'
    room.product_id = 1
    room.member1 = User.objects.get(id=1)
    room.member2 = User.objects.get(id=13)
    room.save()
    # return json of room
    return JsonResponse({'room': room})