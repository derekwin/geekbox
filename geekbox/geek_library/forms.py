from django import forms

# from pagedown.widgets import AdminPagedownWidget  弃用pagedown
from .models import Book

class BookForm(forms.ModelForm):
    # summary=forms.CharField(widget=AdminPagedownWidget())
    pass
