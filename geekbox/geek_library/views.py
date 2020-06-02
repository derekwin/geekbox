from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect,render
from django.urls import reverse
from .models import Book,Genre
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required


def index(request):
    # return HttpResponse('index of library')
    username=request.user.username
    books = Book.objects.all()          
    genres = Genre.objects.all()
    books_list_by_title=books.order_by('title')
    books_list_by_id=books.order_by('-id')
    books_list_by_stars=books.order_by('stars')
    books_latest=[book.title for book in books_list_by_id[:3]]

    context={'books_list_by_title':books_list_by_title,
    'books_list_by_id':books_list_by_id,'books_list_by_stars':books_list_by_stars,
    'genres':genres,'username':username,'books_latest':books_latest}

    return render(request,'geek_library/index.html',context)

@login_required
def book_detail(request,book_id=None):
    if book_id==None:
        return redirect(reverse(index))
    book=Book.objects.get(id=book_id)

    context={'book':book}

    return render(request,'geek_library/book_detail.html',context)
# Create your views here.
