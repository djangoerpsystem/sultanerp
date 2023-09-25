# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('hello/', views.index, name='hello_world'),
    path('test/', views.test, name='test'),

]
