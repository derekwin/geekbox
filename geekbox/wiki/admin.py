from django.contrib import admin
from .models import wiki_instance
# Register your models here.

@admin.register(wiki_instance)
class wiki(admin.ModelAdmin):
    list_display=('name','id')