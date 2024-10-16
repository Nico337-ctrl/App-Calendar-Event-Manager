from django.forms import ModelForm
from django import forms
from dashboard.models.usuarios import User_Perfil

class PerfilCreationForm(forms.ModelForm):
    class Meta:
        model = User_Perfil
        fields = ['perfil_imagen']

    perfil_imagen = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                    
            }
        )
    )