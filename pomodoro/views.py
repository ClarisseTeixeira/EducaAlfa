from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def pomodoro(request):
    return render(request, 'pomodoro/pages/pomodoro.html')

def indexpomodoro(request):
    return render(request, 'pomodoro/pages/indexpomodoro.html')