# Generated by Django 4.2.5 on 2023-12-09 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_alter_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                default="core/static/core/img/personcircle.png", upload_to="perfil/img"
            ),
        ),
    ]
