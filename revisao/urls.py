from django.urls import path
from .views import  detalhes_flashcard, calendario, indexrevisao, flashcards, remover, calendar, flashcard_editar


urlpatterns = [
    path('flashcard/<int:id>/', detalhes_flashcard, name='detalhes_flashcard'),
    path('calendario/', calendario, name='calendario'),
    path('indexrevisao/', indexrevisao, name='indexrevisao'),
    path('flashcards/', flashcards, name='flashcards'),
    path('remover/<int:id>/',remover,name='remover'),
    path('calendar', calendar, name='calendar'),
    path('flashcard/editar/<int:id>/', flashcard_editar, name='flashcard_editar'),

]
 