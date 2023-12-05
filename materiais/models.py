from django.db import models
# Create your models here.

class Disciplina(models.Model):
    nome = models.CharField(max_length=100, default="")


class Assunto(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    nome = models.CharField(max_length=150, default="")

class Conteudo(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    assunto = models.ForeignKey(Assunto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=250)

class Materiais(models.Model):
    conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=250)
    link = models.URLField()
    textotitulo = models.CharField(max_length=250)
    texto = models.TextField()
    referencias = models.TextField()
