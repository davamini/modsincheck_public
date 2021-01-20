from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('<str:mod_name>/', views.mod_info_page, name='mod_info_path'),
]
