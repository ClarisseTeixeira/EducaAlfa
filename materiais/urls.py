from django.urls import path
from .views import * 

urlpatterns = [
    path('disciplinas/', lista_disciplinas, name='lista_disciplinas'),
    path('assuntos/<int:id>/', lista_assuntos, name='lista_assuntos'),
    path('materiais/<int:id>/', lista_materiais, name='lista_materiais'),
    
    path('assuntos/criar/', assunto_criar, name='assunto_criar'),
    path('conteudos/criar/', conteudo_criar, name='conteudo_criar'),
    path('materiais/criar/', materiais_criar, name='materiais_criar'), 
    path('disciplinas/criar/', disciplina_criar, name='disciplina_criar'),
    
    path('materiais/remover/<int:id>/', materiais_remover, name='materiais_remover'),
    path('assuntos/remover/<int:id>/', assunto_remover, name='assunto_remover'),
    path('disciplinas/remover/<int:id>/', disciplina_remover, name='disciplina_remover'),
    path('conteudos/remover/<int:id>/', conteudo_remover, name='conteudo_remover'),
    
    path('materiais/editar/<int:id>/', materiais_editar, name='materiais_editar'),
    path('assuntos/editar/<int:id>/', assunto_editar, name='assunto_editar'),
    path('disciplinas/editar/<int:id>/', disciplina_editar, name='disciplina_editar'),
    path('conteudos/editar/<int:id>/', conteudo_editar, name='conteudo_editar'),

]
