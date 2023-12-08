from django.db import models
from django.contrib.auth.models import User

class Disciplina(models.Model):
    nome = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.nome

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    questoes_certas = models.PositiveIntegerField(default=0)
    questoes_erradas = models.PositiveIntegerField(default=0)

    def taxa_acerto(self):
        num_questoes = self.num_questoes()
        if num_questoes > 0:
            return round((self.questoes_certas / num_questoes) * 100, 2)
        return 0

    def num_questoes(self):
        return self.questoes_certas + self.questoes_erradas
    
    def questoes_certas_disciplina(self, disciplina):
        return Resposta.objects.filter(
            alternativa__questao__disciplina=disciplina,
            user_profile=self,
            certa=True
        ).count()

    def questoes_erradas_disciplina(self, disciplina):
        return Resposta.objects.filter(
            alternativa__questao__disciplina=disciplina,
            user_profile=self,
            certa=False
        ).count()

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