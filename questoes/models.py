from django.db import models
from django.contrib.auth.models import User
class Disciplina(models.Model):
    nome = models.CharField(max_length=100, default="")
    def __str__(self):
        return self.nome
    
class Assunto(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    assunto = models.CharField(max_length=150, default="")
    def __str__(self):
        return self.assunto

class Questao(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    assunto = models.ForeignKey(Assunto, on_delete=models.CASCADE, null=True)  # Defina como nulo temporariamente
    instituicao_ano = models.CharField(max_length=150, default="")
    texto = models.TextField(default="")
    enunciado = models.TextField(default="")
    ordem = models.PositiveIntegerField(default=0) 
    respondida = models.BooleanField(default=False)  

    def __str__(self):
        return f"Questão {self.id} - {self.disciplina.nome}"
    
class Alternativa(models.Model):
    questao = models.ForeignKey('Questao', related_name='alternativas', on_delete=models.CASCADE)
    texto = models.TextField(default="")
    correta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto