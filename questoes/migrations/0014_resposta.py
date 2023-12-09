# Generated by Django 4.2.5 on 2023-12-08 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("questoes", "0013_delete_resposta"),
    ]

    operations = [
        migrations.CreateModel(
            name="Resposta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("certa", models.BooleanField(default=False)),
                (
                    "alternativa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="questoes.alternativa",
                    ),
                ),
                (
                    "user_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="questoes.userprofile",
                    ),
                ),
            ],
        ),
    ]