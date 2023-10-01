from django.shortcuts import render
from .usecases.views.pomodoro_usecases import PomodoroUseCases

def pomodoro(request):
    pomodoro_usecases = PomodoroUseCases()

    if request.method == 'POST':
        # Cria uma nova sessão Pomodoro
        pomodoro_usecases.create_pomodoro_session()

    # Recupera as sessões Pomodoro completadas mais recentes
    sessions = pomodoro_usecases.get_recent_completed_sessions()

    return render(request, 'pomodoro/pomodoro.html', {'sessions': sessions})

