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
                'placeholder': 'Introduce el título de la etiqueta',
                'autofocus': 'autofocus',
            }
        )
    )
    
    descripcion = forms.CharField(
        widget=forms.TextInput(  # Cambié TextInput a Textarea
            attrs={
                'class': 'form-control',
                'placeholder': 'Describe la etiqueta en detalle',
                'rows': 4,  # Esto ajusta la altura del textarea
            }
        )
    )
    
    imagen = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }
        )
    )
