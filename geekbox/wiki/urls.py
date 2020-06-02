from django.urls import path
from . import views

urlpatterns=[
    path('', views.index ,name='wiki_index'),
    path('<str:name>/',views.python_3,name='wiki_py3')
]