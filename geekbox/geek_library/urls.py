from django.urls import path
from . import views

urlpatterns=[
    path('',views.index ,name='library_index'),
    # path('home/',views.home),

    path('detail/',views.book_detail,name='book_detail'),
    path('detail/<int:book_id>',views.book_detail,name='book_detail')
]