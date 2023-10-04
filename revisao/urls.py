from django.urls import path
from .views import form_flashcard,  detalhes_flashcard,  revisoes_por_dia_da_semana,  tudo, calendario, lista_revisao



urlpatterns = [
    path('form_flashcard/', form_flashcard, name="form_flashcard"),
    path('flashcard/<int:flashcard_id>/', detalhes_flashcard, name='detalhes_flashcard'),
    path('lista_revisao', lista_revisao, name='lista_revisao'),
    path('revisoes_por_dia_da_semana/', revisoes_por_dia_da_semana, name='revisoes_por_dia_da_semana'),
    path('calendario', calendario, name='calendario'),
    path('tudo/', tudo, name='tudo'),
]
