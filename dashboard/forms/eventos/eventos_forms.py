from django.forms import ModelForm
from dashboard.models.eventos import Eventos, EtiquetaEvento
from django import forms
from django.contrib.auth.models import Group
from dashboard.models.usuarios import User

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

    # notificar = forms.BooleanField(
    #     label="Notify",
    #     required=False,
    #     initial=True,
    #     widget=forms.CheckboxInput(
    #         attrs={
    #             'class': 'styled-checkbox',
    #             'style': 'width:20px; height:20px;',
    #             'label_suffix': ' '
    #         }
    #     )
    # )


    # opciones=[
    #     ('rol', 'ROLES'),
    #     ('rol_agrupado', 'TODOS LOS USUARIOS DE ROL')
    #     ('usuarios', 'TODOS LOS USUARIOS, USUARIOS O UNICA SELECION')
    # ]
    # notificar_por = forms.MultipleChoiceField(
    #     choices=opciones, 
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Selecciona el filtro'
    #         }
    #     )
    # )

    # notificar_select_multiple = forms.TypedChoiceField(
    #     queryset_correos=User.filtrar_correos,
    #     queryset_correos_rol=User.filtrar_correos_por_rol,
    #     queryset_correos_rol_agrupados=User.filtrar_correos_por_rol_agrupado,

        
    # )
    OPCIONES = [
        ('rol', 'ROLES'),
        ('rol_agrupado', 'TODOS LOS USUARIOS DE UN ROL'),
        ('usuarios', 'TODOS LOS USUARIOS, SELECCIONAR INDIVIDUALMENTE'),
    ]
    notificar_por = forms.ChoiceField(
        choices=OPCIONES,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'filtro_select',  # Usaremos este ID en JavaScript
                'onchange': 'actualizarOpciones()',  # Llamar a la función JS cuando cambie
            }
        ),
        label='Seleccionar Filtro'
    )

    # Segundo campo select (usuarios/roles)
    notificar_select_multiple = forms.MultipleChoiceField(
        choices=[],  # Se llenará dinámicamente con JavaScript
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control',
                'id': 'opciones_select'  # Usaremos este ID en JS para actualizar el campo
            }
        ),
        label='Seleccionar Usuarios o Roles'
    )

    # Campos ocultos con datos prefiltrados (se llenarán en la vista)
    correos_usuarios = forms.MultipleChoiceField(
        choices=[],  # Se llenará con los correos de todos los usuarios
        widget=forms.HiddenInput(),
        required=False,
    )

    correos_rol_agrupado = forms.MultipleChoiceField(
        choices=[],  # Se llenará con correos agrupados por rol
        widget=forms.HiddenInput(),
        required=False,
    )
    
    correos_por_rol = forms.MultipleChoiceField(
        choices=[],  # Se llenará con correos filtrados por roles
        widget=forms.HiddenInput(),
        required=False,
    )