from django.contrib import admin
from .models import Disciplina, Assunto, Questao, Alternativa

admin.site.register(Disciplina)
admin.site.register(Assunto)

class AlternativaInline(admin.TabularInline):
    model = Alternativa

class QuestaoAdmin(admin.ModelAdmin):
    inlines = [AlternativaInline]
    list_display = ('disciplina', 'assunto', 'texto', 'ordem', 'instituicao_ano')
    list_filter = ('disciplina', 'ordem')

admin.site.register(Questao, QuestaoAdmin)