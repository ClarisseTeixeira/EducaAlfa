# Generated by Django 4.2.5 on 2023-12-18 02:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pomodoro", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PomodoroSession",
        ),
    ]
