# app_pomodoro/usecases/serializers/pomodoro_serializers.py
from rest_framework import serializers
from pomodoro.models import PomodoroSession

class PomodoroSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PomodoroSession
        fields = '__all__'
