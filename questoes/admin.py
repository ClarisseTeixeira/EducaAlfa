from django.contrib import admin
from .models import Disciplina, Assunto, Questao, Alternativa, Resposta

admin.site.register(Disciplina)
admin.site.register(Assunto)

class AlternativaInline(admin.TabularInline):
    model = Alternativa

class RespostaInline(admin.TabularInline):
    model = Resposta

class QuestaoAdmin(admin.ModelAdmin):
    inlines = [AlternativaInline, RespostaInline]
    list_display = ('disciplina', 'assunto', 'texto', 'instituicao_ano')
    list_filter = ('disciplina', )

admin.site.register(Questao, QuestaoAdmin)
admin.site.register(Resposta)