from django.db import models
# Create your models here.

class Disciplina(models.Model):
    nome = models.CharField(max_length=100, default="")
    imagem = models.FileField(upload_to='materiais/img/')
    def __str__(self):
        return self.nome


class Assunto(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    nome = models.CharField(max_length=150, default="")
    def __str__(self):
        return self.nome

class Conteudo(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    assunto = models.ForeignKey(Assunto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=250)
    def __str__(self):
        return self.nome
class Materiais(models.Model):
    conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=250)
    link = models.URLField()
    textotitulo = models.CharField(max_length=250)
    texto = models.TextField()
    referencias = models.TextField()
    def __str__(self):
        return self.titulo