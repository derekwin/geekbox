from django.urls import path
from . import views


urlpatterns=[
    path('',views.index,name='chatroom'),
    path('<str:room_name>/',views.index)
]