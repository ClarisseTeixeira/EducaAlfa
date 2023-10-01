from django.db import models


# Create your models here.
class PomodoroSession(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    completed = models.BooleanField(default=False)
