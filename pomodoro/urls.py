from django.urls import path
from . import views

urlpatterns = [
    path('pomodoro/', views.pomodoro, name='pomodoro'),
]
