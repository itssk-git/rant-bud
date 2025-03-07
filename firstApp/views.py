from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q,Count
from .models import Room,Topic,Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def registerPage(request):
    form=UserCreationForm()

    if request.method== "POST":
       form=UserCreationForm(request.POST)
       if form.is_valid():
           form.save(commit=True)
           return redirect('login')

    context={"form": form}
    return render(request,'firstApp/login_register.html',context)




def loginPage(request):
    page='login'

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




    context={'page':page}
    return render(request,'firstApp/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def user_profile(request,pk):
    user=User.objects.get(id=pk)
    rooms=Room.objects.filter(host=user)
    room_counts=rooms.count()
    topics=Topic.objects.all()
    messages=Message.objects.filter(user=user).order_by('-created','-updated')[:8]

    context={"rooms":rooms,"topics":topics,"messages":messages,"room_counts":room_counts}
    return render(request,'firstApp/user_profile.html',context=context)

def home(request):
    page='home'
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    
    rooms=Room.objects.filter(Q(topic__name__icontains=q) |
                              Q(name__icontains=q)|
                              Q(description__icontains=q)
                              )
    topics=Topic.objects.all()
    top_hosts = (
        Room.objects.values('host__id','host__username')
        .annotate(room_count=Count('id'))
        .order_by('-room_count')
    )
   
    
    room_counts=rooms.count()
    messages=Message.objects.all().order_by('-created','-updated')[:8]
    
    

    context={"rooms":rooms,"topics": topics,"room_counts":room_counts,"messages":messages,"hosts":top_hosts,'page':page}
    return render(request,"firstApp/home.html",context=context)
def room(request,pk):

    room=Room.objects.get(id=int(pk))
    is_host = request.user.id == room.host.id
    messages=room.messages.all().order_by("created")

    if request.method=="POST":
        user=request.user
        body=request.POST.get('message')
        message=Message.objects.create(user=user,room=room,body=body)
        message.save()
        room.participants.add(user)
        return redirect('room',pk)
    participants=room.participants.all()
    context={"room":room, "messages":messages,"participants":participants,"is_host":is_host}
    return render(request,"firstApp/room.html",context=context)

@login_required(login_url='login')
def create_room(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            
            return redirect('home')
        
    context={'form':form}
    
    return render(request, 'firstApp/room_form.html',context=context)

@login_required(login_url='login')
def update_room(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.user!= room.host:
        return redirect('home')

    if request.method=="POST":
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save(commit=True)
            return redirect('home')

    context={'form': form}
    return render(request,'firstApp/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room =Room.objects.get(id=pk)
    if request.user!= room.host:
        return redirect('home')
    if request.method=="POST":
        room.delete()
        return redirect('home')
    return render(request,'firstApp/delete.html',{'obj':room})

