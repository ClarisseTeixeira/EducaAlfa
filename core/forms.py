from django.forms import ModelForm
from django import forms
from .models import Profile
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'endereco', 'telefone', 'image']
        