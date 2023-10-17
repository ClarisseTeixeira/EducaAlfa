from django.urls import path
from .views import  detalhes_flashcard,  revisoes_por_dia_da_semana,  tudo, calendario, indexrevisao, flashcards


urlpatterns = [
    path('flashcard/<int:flashcard_id>/', detalhes_flashcard, name='detalhes_flashcard'),
    path('revisoes_por_dia_da_semana/', revisoes_por_dia_da_semana, name='revisoes_por_dia_da_semana'),
    path('calendario', calendario, name='calendario'),
    path('tudo/', tudo, name='tudo'),
    path('indexrevisao', indexrevisao, name='indexrevisao'),
    path('flashcards/', flashcards, name='flashcards')
]
