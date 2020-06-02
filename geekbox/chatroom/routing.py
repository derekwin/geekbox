from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    # path('ws/chatroom/<str:room_name>',consumers.Comsumer),  # room_id
    re_path(r'ws/chatroom/(?P<room_name>\w+)/$',consumers.ChatConsumer), 
]

# Please note that URLRouter nesting will not work properly with path() routes if inner routers are wrapped by additional middleware. 
# https://channels.readthedocs.io/en/latest/topics/routing.html#urlrouter