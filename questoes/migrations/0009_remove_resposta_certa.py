# Generated by Django 4.2.5 on 2023-12-07 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("questoes", "0008_remove_resposta_questoes_certas_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="resposta",
            name="certa",
        ),
    ]