from django.urls import path

from .views import homePageView

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', homePageView, name='home')
]



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('echoapp.urls')),  # Подключили маршруты echoapp
]
