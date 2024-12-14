# bingo/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('user/me/', views.get_current_user, name='current-user'),
]