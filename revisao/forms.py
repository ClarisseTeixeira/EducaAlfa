from django import forms
from .models import Flashcard

class FlashcardForm(forms.ModelForm):

    class Meta:
        model = Flashcard
        fields = (
            'titulo', 'content',
        )