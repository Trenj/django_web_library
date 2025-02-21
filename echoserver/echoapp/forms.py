# echoapp/forms.py
#from django import forms

#class BookForm(forms.Form):
#    title = forms.CharField(max_length=100)
#    author = forms.CharField(max_length=100)


from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price']
