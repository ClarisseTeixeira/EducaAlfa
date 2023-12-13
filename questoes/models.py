from django.db import models
from django.contrib.auth.models import User


class Disciplina(models.Model):
    nome = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.nome

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    acertos = models.IntegerField(default=0)
    erros = models.IntegerField(default=0)

class Assunto(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    assunto = models.CharField(max_length=150, default="")

    def __str__(self):
        return self.assunto

class Questao(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    assunto = models.ForeignKey(Assunto, on_delete=models.CASCADE, null=True)
    instituicao_ano = models.CharField(max_length=150, default="")
    texto = models.TextField(default="")
    enunciado = models.TextField(default="")
    ordem = models.PositiveIntegerField(default=0) 
    respondida = models.BooleanField(default=False)
    questoes_certas = models.PositiveIntegerField(default=0)
    questoes_erradas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Questão {self.id} - {self.disciplina.nome}"

class Alternativa(models.Model):
    questao = models.ForeignKey(Questao, related_name='alternativas', on_delete=models.CASCADE)
    texto = models.TextField(default="")
    correta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto
        
class Resposta(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, null=True)
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    certa = models.BooleanField(default=False)

    def __str__(self):
        return f"Resposta do usuário {self.user_profile.user.username} para a alternativa {self.alternativa.id}"