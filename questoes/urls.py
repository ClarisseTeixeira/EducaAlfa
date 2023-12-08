from django.urls import path
from . import views


urlpatterns = [
    path('questoes/', views.lista_questoes, name='lista_questoes'),    
    path('filtro/', views.filtro_questoes, name='filtro_questoes'),    
    path('verificar_resposta/<int:questao_id>/', views.verificar_resposta, name='verificar_resposta'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    path('indexquestoes', views.indexquestoes, name='indexquestoes'),
    path('grafico/<int:usuario_id>/', views.grafico, name='grafico'),
    path('obter_assuntos/', views.obter_assuntos, name='obter_assuntos'),
    path('questoes/editar/<int:id>/', views.questao_editar, name='questao_editar'),
    path('questoes/criar/', views.questao_criar, name='questao_criar'),
    path('questoes/remover/<int:id>/', views.questao_remover, name='questao_remover'),
]


