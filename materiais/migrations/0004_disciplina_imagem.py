# Generated by Django 4.2.5 on 2023-12-24 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materiais", "0003_remove_disciplina_imagem"),
    ]

    operations = [
        migrations.AddField(
            model_name="disciplina",
            name="imagem",
            field=models.ImageField(
                default=1, upload_to="materiais/static/materiais/img/"
            ),
            preserve_default=False,
        ),
    ]