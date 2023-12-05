from django.forms import ModelForm
from django import forms
from .models import Disciplina, Assunto, Conteudo, Materiais

class DisciplinaForm(ModelForm):
    class Meta:
        model = Disciplina
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AssuntoForm(ModelForm):
    class Meta:
        model = Assunto
        fields = '__all__'
        widgets = {
            'disciplina': forms.Select(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ConteudoForm(ModelForm):
    class Meta:
        model = Conteudo
        fields = '__all__'
        widgets = {
            'disciplina': forms.Select(attrs={'class': 'form-control'}),
            'assunto': forms.Select(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MateriaisForm(ModelForm):
    class Meta:
        model = Materiais
        fields = '__all__'
        widgets = {
            'conteudo': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
            'textotitulo': forms.TextInput(attrs={'class': 'form-control'}),
            'texto': forms.Textarea(attrs={'class': 'form-control'}),
            'referencias': forms.Textarea(attrs={'class': 'form-control'}),
        }
