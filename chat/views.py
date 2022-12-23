from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from .models import Message, Room
from shop.models import Product
from django.core.exceptions import PermissionDenied
from django.http import Http404
import json
from django.contrib.auth import get_user_model

User = get_user_model()

def index(request):
        rooms = Room.objects.filter(member1_id=request.user.id) | Room.objects.filter(member2_id=request.user.id)
        currentroom = rooms.first()
        return render(request, 'chat/chat.html', {
        'avatar': request.user.avatar,
        'room_name_json': mark_safe(json.dumps(currentroom.slug)),
        'username': mark_safe(json.dumps(request.user.name)),
        'user_id': mark_safe(json.dumps(request.user.id)),
        'room_id': mark_safe(json.dumps(currentroom.id)),
        'currentroom': currentroom,
        'second_user': currentroom.get_second_user(request.user),
        'rooms': rooms,
    })

@login_required
def room(request, room_name):
    # check room if exist
    if not Room.objects.filter(slug=room_name).exists():
        raise Http404('message: Room does not exist')
    # check if user is in the room
    room = Room.objects.get(slug=room_name)
    if not room.check_user(request.user):
        raise PermissionDenied("You are not in the room")
    # get all rooms of user
    rooms = Room.objects.filter(member1_id=request.user.id) | Room.objects.filter(member2_id=request.user.id)
    return render(request, 'chat/room.html', {
        'avatar': request.user.avatar,
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.name)),
        'user_id': mark_safe(json.dumps(request.user.id)),
        'room_id': mark_safe(json.dumps(room.id)),
        'currentroom': room,
        'second_user': room.get_second_user(request.user),
        'rooms': rooms,
    })
def create(request):
    if request.method == 'POST':
        # get product from post
        product_id = request.POST['product']
        print(product_id)
        product = Product.objects.get(id=request.POST['product'])
        user2 = User.objects.get(id=request.POST['user_2'])
        # check if user_2 exist and product does not exist
        if not user2 or not product:
            raise Http404('message: User or Product does not exist')
        # check if user_2 is not the same as user_1
        if request.user == user2:
            raise PermissionDenied("You can't chat with yourself")
        # check if user_1 is not the seller
        if request.user == product.owner:
            raise PermissionDenied("You can't chat with the seller")
        # check if user_2 is the seller
        if user2 == product.owner:
            # check if room exist based of user_1 and user_2 and product and redirect if exist
            if Room.objects.filter(member1_id=request.user.id, member2_id=user2.id, product=product).exists():
                room = Room.objects.get(member1_id=request.user.id, member2_id=user2.id, product=product)
                return redirect('room', room_name=room.slug)
            room = Room()
            room.member1_id = request.user.id
            room.member2_id = user2.id
            room.product = product
            room.save()
            if room:
                # redirect to the room using slug and url name
                return redirect('room', room_name=room.slug)
