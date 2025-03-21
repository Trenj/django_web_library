from django.db import models
from django.contrib.auth.models import AbstractUser
import json

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def is_admin(self):
        return self.role == 'admin'

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    author = models.CharField(max_length=100, verbose_name='Автор')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.JSONField(default=dict)

    def get_items(self):
        return self.items or {}

    def set_items(self, items):
        self.items = items
        self.save()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.JSONField(default=dict)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def set_items(self, cart_items):
        self.items = json.dumps(cart_items)

    def get_items(self):
        return json.loads(self.items)

    class Meta:
        ordering = ['-created_at']
