from django import views
from django.urls import path
from users.views import *
from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from mywebsite.settings import *
from django.conf.urls import handler404, handler500
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', users, name='list_users'),
    path('register/', registrasi_add, name='registrasi_add'),
    path('view/<int:id>',users_view, name='users_view'),
    path('update/<int:id>',users_update, name='users_update'),
    path('delete/<int:id>',users_delete, name='users_delete'),
]