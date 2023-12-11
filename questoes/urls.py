from django.urls import path
from . import views


urlpatterns = [
    path('questoes/', views.lista_questoes, name='lista_questoes'),    
    path('verificar_resposta/', views.verificar_resposta, name='verificar_resposta'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    path('indexquestoes', views.indexquestoes, name='indexquestoes'),
    path('obter_assuntos/', views.obter_assuntos, name='obter_assuntos'),
    path('questoes/editar/<int:id>/', views.questao_editar, name='questao_editar'),
    path('questoes/criar/', views.questao_criar, name='questao_criar'),
    path('questoes/remover/<int:id>/', views.questao_remover, name='questao_remover'),



    path('formulariodequestoes/', views.formulario_questoes, name='formulario_questoes'),
    path('processar_respostas/', views.processar_respostas, name='processar_respostas'),
    path('resultados/', views.resultados, name='resultados'),
]

 
