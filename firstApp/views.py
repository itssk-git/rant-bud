from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q
from .models import Room,Topic
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def loginPage(request):

    if request.method== 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"User doesnt exist")
        user= authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials")




    context={}
    return render(request,'firstApp/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    
    rooms=Room.objects.filter(Q(topic__name__icontains=q) |
                              Q(name__icontains=q)|
                              Q(description__icontains=q)
                              )
    topics=Topic.objects.all()
    room_counts=rooms.count()
    

    context={"rooms":rooms,"topics": topics,"room_counts":room_counts}
    return render(request,"firstApp/home.html",context=context)
def room(request,pk):
    room=Room.objects.get(id=int(pk))
    context={"room":room}
    return render(request,"firstApp/room.html",context=context)

def create_room(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('home')
        
    context={'form':form}
    
    return render(request, 'firstApp/room_form.html',context=context)

def update_room(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.method=="POST":
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save(commit=True)
            return redirect('home')

    context={'form': form}
    return render(request,'firstApp/room_form.html',context)


def deleteRoom(request,pk):
    room =Room.objects.get(id=pk)
    if request.method=="POST":
        room.delete()
        return redirect('home')
    return render(request,'firstApp/delete.html',{'obj':room})

