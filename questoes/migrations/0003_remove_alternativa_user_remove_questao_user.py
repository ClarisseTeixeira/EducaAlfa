# Generated by Django 4.2.5 on 2023-10-02 02:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("questoes", "0002_alternativa_user_questao_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="alternativa",
            name="user",
        ),
        migrations.RemoveField(
            model_name="questao",
            name="user",
        ),
    ]
