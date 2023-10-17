from django.urls import path
from . import views

urlpatterns = [
    path('disciplinas/', views.lista_disciplinas, name='lista_disciplinas'),
    path('assuntos/<int:id>/', views.lista_assuntos, name='lista_assuntos'),
    path('materiais/<int:id>/', views.lista_materiais, name='lista_materiais'),
]
