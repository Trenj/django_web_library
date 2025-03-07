from django import forms
from .models import Book

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'image']


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role"]

class LoginForm(AuthenticationForm):
    pass
