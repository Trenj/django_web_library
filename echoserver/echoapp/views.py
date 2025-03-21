from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from decimal import Decimal
from .forms import RegisterForm, LoginForm, BookForm, UserProfileForm
from .models import Book, Order, Cart

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создаем корзину для нового пользователя
            Cart.objects.create(user=user)
            login(request, user)
            return redirect("book_list")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("book_list")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("book_list")

# Проверка, является ли пользователь администратором
def is_admin(user):
    return user.is_authenticated and getattr(user, 'role', None) == "admin"

@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'echoapp/bookstore.html', {'form': form, 'title': 'Добавить книгу', 'view_type': 'form'})

@login_required
@user_passes_test(is_admin)
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'echoapp/bookstore.html', {'form': form, 'title': 'Редактировать книгу', 'view_type': 'form'})

@login_required
@user_passes_test(is_admin)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'echoapp/bookstore.html', {'book': book, 'view_type': 'delete'})

def book_list(request):
    books = Book.objects.all()
    return render(request, "echoapp/book_list.html", {"books": books})

# Новые представления для профиля, корзины и заказов

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'echoapp/profile.html', {
        'form': form
    })

@login_required
def add_to_cart(request, book_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        book = get_object_or_404(Book, id=book_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.get_items()
        
        if str(book_id) in items:
            items[str(book_id)]['quantity'] += 1
        else:
            items[str(book_id)] = {
                'quantity': 1,
                'title': book.title,
                'price': str(book.price)
            }
        
        cart.set_items(items)
        cart_total = sum(Decimal(item['price']) * item['quantity'] for item in items.values())
        
        return JsonResponse({
            'success': True,
            'cart_total': str(cart_total),
            'cart_items': len(items)
        })
    return JsonResponse({'success': False})

@login_required
def remove_from_cart(request, book_id):
    cart = Cart.objects.get(user=request.user)
    items = cart.get_items()
    if str(book_id) in items:
        del items[str(book_id)]
        cart.set_items(items)
    return redirect('cart')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.get_items()
    
    # Вычисляем общую стоимость для каждого товара
    for item in items.values():
        item['total'] = str(Decimal(item['price']) * item['quantity'])
    
    total = sum(Decimal(item['price']) * item['quantity'] for item in items.values())
    
    return render(request, 'echoapp/cart.html', {
        'cart': items,
        'total': total
    })

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.get_items()
    if not items:
        messages.error(request, 'Ваша корзина пуста')
        return redirect('cart')
    
    total = sum(Decimal(item['price']) * item['quantity'] for item in items.values())
    
    order = Order.objects.create(
        user=request.user,
        items=items,
        total_price=total
    )
    
    # Очищаем корзину
    cart.set_items({})
    
    messages.success(request, 'Заказ успешно создан')
    return redirect('orders')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'echoapp/orders.html', {'orders': orders})
