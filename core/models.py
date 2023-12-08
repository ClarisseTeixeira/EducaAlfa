from django.db import models

# Create your models here.

class Perfil(models.Model):
    email = models.EmailField()
    telefone = models.CharField(max_length=11)
    Endereco = models.CharField(max_length=200)
    foto = models.ImageField()
