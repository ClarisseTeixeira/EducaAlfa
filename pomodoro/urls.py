from django.urls import path
from .views import pomodoro, indexpomodoro

urlpatterns = [
    path('pomodoro/', pomodoro, name='pomodoro'),
    path('indexpomodoro/', indexpomodoro, name='indexpomodoro'),
]