from django.shortcuts import render
from .models import wiki_instance

# Create your views here.
def index(request):
    return render(request,'wiki/index.html')

def python_3(request,name):
    markdown=wiki_instance.objects.get(name=name)
    context={
        'markdown':markdown,
    }
    return render(request,'wiki/python3.html',context)