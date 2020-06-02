from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.

def index(request,room_name=None):
    if room_name:
        return render(request,'chatroom/chatroom.html',{
            'room_name':room_name,
        })
    else:
        return render(request,'chatroom/index.html')
