from django.contrib import admin
from .models.Stikers import Stiker,Topic
from .models.Users import StikerUser
from .models.Comments import Comment,Reply

from .forms import CreateComment,CreateReply,CreateStiker

@admin.register(StikerUser)
class StikerUserAdmin(admin.ModelAdmin):
    list_display=('username','Gender','email','Icon')


@admin.register(Stiker)
class StikerAdmin(admin.ModelAdmin):
    form = CreateStiker
    list_display=('title','display_topics')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display=('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    form = CreateComment
    list_display=('stiker','author','comment','id')

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    form = CreateReply
    list_display=('comment','parent','parent','author','reply')