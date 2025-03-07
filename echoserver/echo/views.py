from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from .models import User

def homePageView(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вход выполнен успешно!')
                return redirect('home')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def is_admin(user):
    return user.role == 'admin'

@login_required
def add_book(request):
    if request.user.role == 'admin' or request.user.role == 'user':
        # Здесь будет логика добавления книги
        return render(request, 'add_book.html')
    return redirect('home')

@user_passes_test(is_admin)
def edit_book(request, book_id):
    # Здесь будет логика редактирования книги
    return render(request, 'edit_book.html')

@user_passes_test(is_admin)
def delete_book(request, book_id):
    # Здесь будет логика удаления книги
    return redirect('home')