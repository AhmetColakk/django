from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required 
from .models import Room, Topic
from django.contrib.auth.models import User
from .forms import RoomForm

# Create your views here.

# rooms = [ 
#          {"id": 1, "name": "Learn Pyhton",},
#          {"id": 2, "name": "Learn CSS",},
#          {"id": 3, "name": "Learn HTML",},
#          {"id": 4, "name": "Learn JS",},
#          ]

def login_page(request,):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
     
        
        try:
          user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("base:home")
    context = {}
    return render(request, "base/login_register.html", context )
    

def logout_page(request):
    logout(request)
    return redirect("base:home")
    


def home(request):
    q = request.GET.get("q") if request.GET.get("q") else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
        
        )
    rooms_count = rooms.count()
    topics = Topic.objects.all()
    context = { "rooms": rooms, "topics": topics, "rooms_count": rooms_count} 
    return render(request, "base/home.html", context)


def room(request, pk):
    # get_room_by_id = [ room  for room in rooms if str(room["id"]) == pk]
    # room = get_room_by_id[0] if get_room_by_id else None
    # context = None
    # try:
    #   room = Room.objects.get(id=pk)
    #   context = { "room": room } if room else None
    # except :
    #   print('No item matched')
  
    room = get_object_or_404(Room, pk=pk)
    context = { "room": room }
  
    return render(request, "base/room.html", context)

@login_required(login_url="base:login")
def create_room(request):
    form = RoomForm()
    
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("base:home")
        
    context = { "form" : form }
    return render(request, "base/room_form.html", context )

@login_required(login_url="base:login")
def update_room(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)
    if request.user is not room.host:
        return HttpResponse("You are allowed here")
    
    
    if request.POST:
        form = RoomForm(request.POST, instance=room)
        
        if form.is_valid:
            form.save()       
            return redirect("base:home")
        
    context = {"form": form}
    return render(request, "base/room_form.html", context)
    
@login_required(login_url="base:login")
def delete_room(request, id):
    room = Room.objects.get(id=id)
    
    if request.method == "POST":
        print(request.user, room.host)
        if request.user == room.host:
            room.delete()
            return redirect("base:home")
        else:       
            return HttpResponse("You are not allowed here")    
    return render(request, "base/delete.html", {"obj":room})
    