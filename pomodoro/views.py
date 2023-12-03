from django.shortcuts import render
from datetime import datetime, timedelta
from .models import PomodoroSession
from django.contrib.auth.decorators import login_required

@login_required
def pomodoro(request):
    if request.method == 'POST':

        
        
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=25)
        PomodoroSession.objects.create(start_time=start_time, end_time=end_time)

    sessions = PomodoroSession.objects.filter(completed=True).order_by('-start_time')[:4]
    
    return render(request, 'pomodoro/pages/pomodoro.html', {'sessions': sessions})

def indexpomodoro(request):
    return render(request, 'pomodoro/pages/indexpomodoro.html')