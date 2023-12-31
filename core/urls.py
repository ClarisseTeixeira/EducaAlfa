"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib.auth import views as auth_views 
from .views.home import index, dashboard, revisoes, arearestrita
from .views.auth import *

urlpatterns = [
    path('accounts/login/', user_login, name='login'),
    path('accounts/logout/', user_logout, name='logout'),
    path('registro/', registro, name='registro'),
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('revisoes/', revisoes, name='revisoes'),
    path('arearestrita/',arearestrita, name='arearestrita'),
    path('profile/', profile, name='profile'),

]  