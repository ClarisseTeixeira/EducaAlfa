from django.urls import path
from .views import lista_questoes, verificar_resposta, estatisticas, indexquestoes, obter_assuntos,grafico


urlpatterns = [
    path('questoes/', lista_questoes, name='lista_questoes'),    
    path('verificar_resposta/', verificar_resposta, name='verificar_resposta'),
    path('estatisticas/', estatisticas, name='estatisticas'),
    path('indexquestoes', indexquestoes, name='indexquestoes'),
    path('obter_assuntos/', obter_assuntos, name='obter_assuntos'),
    path('grafico', grafico, name='grafico'),
]

 
