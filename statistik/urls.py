# statistik/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.index, name='hello_world'),
]
