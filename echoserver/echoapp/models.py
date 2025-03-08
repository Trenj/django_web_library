from django.db import models
from django.contrib.auth.models import AbstractUser

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
