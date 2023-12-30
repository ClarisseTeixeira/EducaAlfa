from django.urls import path
from .views import   indexrevisao, flashcards, remover,  flashcard_editar, detalhes_flashcard, calendario, calendar


urlpatterns = [
    path('indexrevisao/', indexrevisao, name='indexrevisao'),
    path('flashcards/', flashcards, name='flashcards'),
    path('remover/<int:id>/',remover,name='remover'),
    path('flashcard/editar/<int:id>/', flashcard_editar, name='flashcard_editar'),
    path('flashcard/<int:id>/', detalhes_flashcard, name='detalhes_flashcard'),
    path('calendario/', calendario, name='calendario'),
    path('calendar/', calendar, name='calendar'),
]
 