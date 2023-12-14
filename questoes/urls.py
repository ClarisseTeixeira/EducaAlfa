from django.urls import path
from . import views


urlpatterns = [
    path('questoes/', views.lista_questoes, name='lista_questoes'),    
    path('verificar_resposta/', views.verificar_resposta, name='verificar_resposta'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    path('indexquestoes', views.indexquestoes, name='indexquestoes'),
    path('obter_assuntos/', views.obter_assuntos, name='obter_assuntos'),
    path('grafico', views.grafico, name='grafico'),
]

 
