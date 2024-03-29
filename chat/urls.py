from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='chat-index'),
    path('room/<str:room_name>/', views.room, name='room'),
    path('create/', views.create, name='create_chat_room'),
]