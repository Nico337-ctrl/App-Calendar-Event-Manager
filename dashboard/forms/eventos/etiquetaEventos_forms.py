from django.forms import ModelForm
from dashboard.models.eventos import EtiquetaEvento
from django import forms

class EtiquetaEventoForm(forms.ModelForm):
    class Meta:
        model = EtiquetaEvento
        fields = ['titulo', 'descripcion', 'imagen']
    
    titulo = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
    descripcion = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'type': 'image',
            }
        )
    )