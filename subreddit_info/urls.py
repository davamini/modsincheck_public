from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('<str:subreddit_name>/', views.subreddit_info_page, name='subreddit_info_path'),
]