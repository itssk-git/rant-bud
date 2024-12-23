from django.shortcuts import render,redirect
from .models import Room
from .forms import RoomForm

# Create your views here.
def main(request):
    return render(request,"main.html")
def home(request):
    rooms=Room.objects.all()
    context={"rooms":rooms}
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
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('home')

    context={'form': form}
    return render(request,'firstApp/room_form.html',context)

