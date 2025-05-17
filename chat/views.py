from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Room, Message
from .forms import RoomForm
from django.db.models import Q

@login_required
def home(request):
    """
    Displays the home page with a list of available chat rooms.
    """
    rooms = Room.objects.all()
    return render(request, 'chat/home.html', {'rooms': rooms})

@login_required
def create_room(request):
    """
    Handles the creation of a new chat room.
    """
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['name']
            # Check if a room with this name already exists
            if Room.objects.filter(name=room_name).exists():
                form.add_error('name', 'A room with this name already exists.')
                return render(request, 'chat/create_room.html', {'form': form})

            room = Room.objects.create(name=room_name)
            room.users.add(request.user)  # Add the creator to the room
            return redirect('chat:room', room_id=room.id)
        else:
            return render(request, 'chat/create_room.html', {'form': form})
    else:
        form = RoomForm()
        return render(request, 'chat/create_room.html', {'form': form})

@login_required
def room(request, room_id):
    """
    Displays a specific chat room and its messages.
    """
    room = get_object_or_404(Room, id=room_id)

    # Check if the user is in the room
    if not room.users.filter(id=request.user.id).exists():
        # Add user to the room.  Important for allowing the user to see messages
        room.users.add(request.user)

    messages = Message.objects.filter(room=room).order_by('timestamp')
    return render(request, 'chat/room.html', {'room': room, 'messages': messages})

@login_required
def join_room(request, room_id):
    """
    Allows a user to join an existing chat room.
    """
    room = get_object_or_404(Room, id=room_id)
    user = request.user

    if room.users.filter(id=user.id).exists():
        return redirect('chat:room', room_id=room.id)  # User is already in the room

    room.users.add(user)
    return redirect('chat:room', room_id=room.id)

@login_required
def leave_room(request, room_id):
    """
    Allows a user to leave a chat room.
    """
    room = get_object_or_404(Room, id=room_id)
    user = request.user

    if room.users.filter(id=user.id).exists():
        room.users.remove(user)
    return redirect('chat:home')

def search_rooms(request):
    """
    Handles searching for rooms.
    """
    query = request.GET.get('q', '')
    results = Room.objects.filter(Q(name__icontains=query))
    return render(request, 'chat/search_results.html', {'results': results, 'query': query})