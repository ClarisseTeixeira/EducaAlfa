# Generated by Django 4.2.5 on 2023-12-07 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("questoes", "0010_resposta_certa"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Resposta",
        ),
    ]