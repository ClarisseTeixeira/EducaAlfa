from django.forms import ModelForm
from django import forms
from .models import Perfil

class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
        widgets = {
            'conteudo': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
            'textotitulo': forms.TextInput(attrs={'class': 'form-control'}),
            'texto': forms.Textarea(attrs={'class': 'form-control'}),
            'referencias': forms.Textarea(attrs={'class': 'form-control'}),
        }
