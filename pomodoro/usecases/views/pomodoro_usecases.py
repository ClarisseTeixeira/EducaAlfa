from datetime import datetime, timedelta
from pomodoro.models import PomodoroSession

class PomodoroUseCases:
    def create_pomodoro_session(self):
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=25)
        PomodoroSession.objects.create(start_time=start_time, end_time=end_time)

    def get_recent_completed_sessions(self):
        sessions = PomodoroSession.objects.filter(completed=True).order_by('-start_time')[:4]
        return sessions