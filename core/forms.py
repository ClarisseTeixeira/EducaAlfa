from django.forms import ModelForm
from django import forms
from .models import Perfil

class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }
