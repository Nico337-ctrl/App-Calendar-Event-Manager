from django.forms import ModelForm
from dashboard.models.eventos import Eventos
from django import forms

class FormEventos(forms.ModelForm):
    class Meta:
        model = Eventos
        fields = ['titulo', 'descripcion', 'info_extra', 'inicia_el', 'termina_el']
    
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
    
    info_extra = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    
    inicia_el = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'type' : 'datetime-local'
            }
        )
    )
    termina_el = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'type' : 'datetime-local'
            }
        )
    )