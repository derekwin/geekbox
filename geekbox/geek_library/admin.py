from django.contrib import admin
from .models import Book,Author,Genre

admin.site.site_title="Geekbox后台管理"
admin.site.site_header="Geekbox后台管理系统"

from .forms import BookForm

# Register your models here.
# admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form=BookForm
    list_display = ('title','display_author','display_genre','stars')
    search_fields=('title',)
    list_filter = ('stars',)    

    # fieldsets=(
    #     (

    #     ),

    # )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=('name','birth_year','display_books')
    search_fields=('name',)
    # fields=('name',('data_birth','data_death'))

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields=('name',)


# admin.site.register(Book,BookAdmin)

# admin.site.register(Author,AuthorAdmin)