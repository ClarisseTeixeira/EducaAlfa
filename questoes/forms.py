from django import forms
from .models import Questao, Alternativa

from django import forms
from .models import Questao, Alternativa

class QuestaoForm(forms.ModelForm):
    alternativa1 = forms.CharField(max_length=255, label='Alternativa 1', widget=forms.TextInput(attrs={'class': 'form-control'}))
    alternativa2 = forms.CharField(max_length=255, label='Alternativa 2', widget=forms.TextInput(attrs={'class': 'form-control'}))
    alternativa3 = forms.CharField(max_length=255, label='Alternativa 3', widget=forms.TextInput(attrs={'class': 'form-control'}))
    alternativa_correta = forms.ChoiceField(choices=[('1', 'Alternativa 1'), ('2', 'Alternativa 2'), ('3', 'Alternativa 3')],
                                            label='Alternativa Correta', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Questao
        fields = ['disciplina', 'assunto', 'instituicao_ano', 'texto', 'enunciado', 'ordem', 'respondida', 'questoes_certas', 'questoes_erradas']
        widgets = {
            'disciplina': forms.Select(attrs={'class': 'form-control'}),
            'assunto': forms.Select(attrs={'class': 'form-control'}),
            'instituicao_ano': forms.TextInput(attrs={'class': 'form-control'}),
            'texto': forms.Textarea(attrs={'class': 'form-control'}),
            'enunciado': forms.Textarea(attrs={'class': 'form-control'}),
        }
class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = '__all__'
        widgets = {
            'questao': forms.Select(attrs={'class': 'form-control'}),
            'texto': forms.Textarea(attrs={'class': 'form-control'}),
            'correta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

