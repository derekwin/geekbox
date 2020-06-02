from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='cms'),
    # path('home/',views.home),

    path('detail/',views.detail,name='detail'),
    path('detail/<int:cms_id>/',views.detail,name='detail'),

    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),

    path('userpage/',views.userPage,name='userpage'),
    path('userpage/<str:username>/',views.userPage,name='userpage'),
    path('update_user/<int:user_id>/',views.update_user,name='update_user'),

    path('topic/',views.topicPage,name='topicpage'),
    path('topic/<str:topic_name>/',views.topicPage,name='topicpage'),

    path('post_comment/<int:stiker_id>',views.post_comment,name='post_comment'),
    path('update_comment/<int:comment_id>/',views.update_comment,name='update_comment'),
    path('delete_comment/<int:comment_id>/',views.delete_comment,name='delete_comment'),

    path('post_reply/<int:comment_id>/',views.post_reply,name='post_reply'),
    path('post_reply/<int:comment_id>/<int:parent_id>/',views.post_reply,name='post_reply'),
    path('update_reply/<int:reply_id>/',views.update_reply,name='update_reply'),
    path('delete_reply/<int:reply_id>/',views.delete_reply,name='delete_reply'),

    path('create/',views.create_stiker,name='create_stiker'),
    path('update/<int:stiker_id>/',views.update_stiker,name='update_stiker'),
    path('delete/<int:stiker_id>/',views.delete_stiker,name='delete_stiker'),

    path('star/<str:type>/<int:id>/',views.star,name='star'),
    path('unstar/<str:type>/<int:id>/',views.unstar,name='unstar'),

]