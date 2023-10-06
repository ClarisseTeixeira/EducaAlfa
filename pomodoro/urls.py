from django.urls import path
from . import views

urlpatterns = [
    path('pomodoro', views.pomodoro, name='pomodoro'),
    path('intro', views.intro, name='intro'),
]