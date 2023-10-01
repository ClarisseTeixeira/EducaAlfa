from django.core import serializers
from pomodoro.models import PomodoroSession

class PomodoroSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PomodoroSession
        fields = '__all__'
