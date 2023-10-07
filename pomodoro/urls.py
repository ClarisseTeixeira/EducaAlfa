from django.urls import path
from . import views

urlpatterns = [
    path('pomodoro', views.pomodoro, name='pomodoro'),
    path('indexpomodoro', views.indexpomodoro, name='indexpomodoro'),
]