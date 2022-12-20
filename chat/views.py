from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import Message, Room
from django.core.exceptions import PermissionDenied
from django.http import Http404
import json

def index(request):
    return render(request, 'chat/index.html', {})

@login_required
def room(request, room_name):
    # check room if exist
    if not Room.objects.filter(slug=room_name).exists():
        raise Http404('message: Room does not exist')
    # check if user is in the room
    room = Room.objects.get(slug=room_name)
    if not room.check_user(request.user):
        raise PermissionDenied("You are not in the room")
    return render(request, 'chat/room.html', {
        'avatar': request.user.avatar,
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.name)),
        'user_id': mark_safe(json.dumps(request.user.id)),
        'room_id': mark_safe(json.dumps(room.id)),
    })