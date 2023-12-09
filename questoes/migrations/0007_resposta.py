# Generated by Django 4.2.5 on 2023-12-07 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("questoes", "0006_userprofile"),
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
                ("questoes_certas", models.PositiveIntegerField(default=0)),
                ("questoes_erradas", models.PositiveIntegerField(default=0)),
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