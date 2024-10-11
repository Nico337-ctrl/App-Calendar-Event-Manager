from django.forms import ModelForm
from django import forms
from dashboard.models.eventos import Eventos
from dashboard.models.usuarios import User
# from dashboard.models.eventos import Eventos, EtiquetaEvento
# from django.contrib.auth.models import Group


OPCIONES = [
        ('rol', 'ROLES'),
        ('rol_agrupado', 'TODOS LOS USUARIOS DE UN ROL'),
        ('usuarios', 'TODOS LOS USUARIOS, SELECCIONAR INDIVIDUALMENTE'),
]
class FormEventosNotificacion(forms.Form):

    
    filtro = forms.ChoiceField(
        choices=OPCIONES,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        label='Seleccionar Filtro'
    )

    select_usuarios_por_correo = forms.ModelChoiceField(queryset=User.objects.all(), to_field_name='email')

    select_usuarios_por_correo_rol = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control',
            }
        ),
        label='Seleccionar Usuarios o Roles',
        required=False
    )
    
    select_usuarios_por_correo_rol_agrupado = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control',
            }
        ),
        label='Seleccionar Usuarios o Roles',
        required=False
    )
    
    # def __init__(self, *args, **kwargs):
    #     super(FormEventosNotificacion, self).__init__(*args, **kwargs)
        
    #     # Asignar el queryset al campo notificar_select_multiple
    #     self.fields['select_usuarios_por_correo'].choices = [
    #         (user) for user in User.filtrar_correos()
    #     ]
        
        # self.fields['select_usuarios_por_correo_rol'].choices = [
        #     (user) for user in User.filtrar_correos_por_rol()
        # ]
        
        # self.fields['select_usuarios_por_correo_rol_agrupado'].choices = [
        #     (user) for user in User.filtrar_correos_por_rol_agrupado()
        # ]
        
        