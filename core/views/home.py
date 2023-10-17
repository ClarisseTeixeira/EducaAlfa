from django.shortcuts import render, redirect

def index(request):
    return render(request, "index.html")




def home(request):
    return render(request, "core/home.html")


def dashboard(request):
    return render(request, "core/pages/dashboard.html")