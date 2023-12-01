from django.urls import path
from . import views

urlpatterns = [
    path('questoes/', views.lista_questoes, name='lista_questoes'),    
    path('filtro/', views.filtro_questoes, name='filtro_questoes'),    
    path('verificar_resposta/<int:questao_id>/', views.verificar_resposta, name='verificar_resposta'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    path('indexquestoes', views.indexquestoes, name='indexquestoes'),
    path('grafico/<int:usuario_id>/', views.grafico, name='grafico'),
]
