from django.utils import timezone
from django.db import models
from django_quill.fields import QuillField
from django.contrib.auth.models import User

class Flashcard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=150)
    content = QuillField()
    data = models.DateField(default=timezone.now)
 
class Revisao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    data_agendada = models.DateField()
    concluida = models.BooleanField(default=False)  
