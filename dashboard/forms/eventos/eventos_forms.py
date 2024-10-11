from django.forms import ModelForm
from dashboard.models.eventos import Eventos, EtiquetaEvento
from django import forms


class FormEventos(forms.ModelForm):
    class Meta:
        model = Eventos
        fields = ['titulo', 'descripcion', 'info_extra', 'inicia_el', 'termina_el', 'etiqueta']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['etiqueta'].label_from_instance = lambda obj: obj.titulo

    titulo = forms.CharField(
        label="Name *",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Tu titulo de evento'
            }
        )
    )
    
    descripcion = forms.CharField(
        label="Message *",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Describe el evento a detalle'
            }
        )
    )
    
    info_extra = forms.CharField(
        label="Budget",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Informacion extra sobre el evento'
            }
        )
    )
    
    inicia_el = forms.DateTimeField(
        label="Start Date",
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }
        )
    )
    
    termina_el = forms.DateTimeField(
        label="End Date",
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }
        )
    )
    
    etiqueta = forms.ModelChoiceField(
        label="Tag",
        queryset=EtiquetaEvento.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Etiqueta a utilizar para el evento'
            }
        )
    )

