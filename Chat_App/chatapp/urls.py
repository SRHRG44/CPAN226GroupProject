from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_room_list, name='chat_room_list'),
     path('create_or_join/', views.create_or_join_room, name='create_or_join_room'), 
    path('<str:room_name>/', views.chat_room_detail, name='chat_room_detail'),
    path('<str:room_name>/send/', views.send_message, name='send_message'),
    path('message/<int:message_id>/read/', views.mark_message_read, name='mark_message_read'),
]