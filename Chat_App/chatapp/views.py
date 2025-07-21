from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatRoom, Message
from django.db.models import Q

@login_required
def chat_room_list(request):
    chat_rooms = ChatRoom.objects.filter(participants=request.user)
    return render(request, 'chatapp/chat_room_list.html', {'chat_rooms': chat_rooms})

@login_required
def create_or_join_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            # Get or create the chat room
            # .get_or_create() returns (object, created_boolean)
            chat_room, created = ChatRoom.objects.get_or_create(name=room_name)

            # Add the current user to the chat room's participants
            chat_room.participants.add(request.user)
            # You might want a message indicating if it was created or joined

            # Redirect to the detail page of the room
            return redirect('chat_room_detail', room_name=chat_room.name)
    # If not a POST request or no room_name, redirect back to the list
    return redirect('chat_room_list')

@login_required
def chat_room_detail(request, room_name):
    chat_room = get_object_or_404(ChatRoom, name=room_name)
    if request.user not in chat_room.participants.all():
        # Optionally add user to room or redirect
        return redirect('chat_room_list') # Redirect if user is not a participant

    messages = chat_room.messages.all()
    # Mark messages as delivered when viewed
    messages.filter(is_delivered=False).update(is_delivered=True)
    return render(request, 'chatapp/chat_room_detail.html', {'chat_room': chat_room, 'messages': messages})

@login_required
def send_message(request, room_name):
    if request.method == 'POST':
        chat_room = get_object_or_404(ChatRoom, name=room_name)
        content = request.POST.get('content')
        if content:
            Message.objects.create(chat_room=chat_room, sender=request.user, content=content)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)

@login_required
def mark_message_read(request, message_id):
    if request.method == 'POST':
        message = get_object_or_404(Message, id=message_id)
        # Ensure only intended recipient can mark as read (more complex logic for 1-to-1 chats)
        # For group chats, anyone seeing it could potentially mark it as read.
        # For a basic demo, we'll just mark it read.
        if not message.is_read:
            message.is_read = True
            message.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)