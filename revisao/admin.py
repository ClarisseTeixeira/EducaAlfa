from django.contrib import admin
from .models import Flashcard, Revisao

# Register your models here.

@admin.register(Revisao)
class RevisaodAdmin(admin.ModelAdmin):
    list_display=['data_agendada','concluida']


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display=['titulo', 'content',]
    pass

