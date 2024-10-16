from django.forms import ModelForm
from django import forms
from dashboard.models.usuarios import User
from django.contrib.auth.models import Group
# from dashboard.models.eventos import Eventos, EtiquetaEvento



OPCIONES = [
        ('rol_agrupado', 'TODOS LOS USUARIOS DE UN ROL'),
        ('usuarios', 'TODOS LOS USUARIOS, SELECCIONAR INDIVIDUALMENTE'),
]
class FormEventosNotificacion(forms.Form):

    
    filtro = forms.ChoiceField(
        choices=OPCIONES,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'filtro-select',  # Agregamos un id para controlarlo con JS
            }
        ),
        label='Seleccionar Filtro'
    )

    
    filtro_rol = forms.ChoiceField(
        choices=[],  # Se inicializa vacío
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'filtro-rol',
            }
        ),
        required=False,
        label='Seleccionar Rol'
    )

    filtro_usuarios_email = forms.MultipleChoiceField(
        choices=[],  # Se inicializa vacío
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control',
                'id': 'filtro-usuarios',
            }
        ),
        required=False,
        label='Seleccionar Usuarios'
    )
    # filtro_rol_usuarios = forms.ModelChoiceField(
    #     queryset=Group.objects.all(),
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control',
    #             'id': 'filtro-rol',  # Agregamos un id para controlarlo con JS
    #         }
    #     ),
    #     required=False,
    #     label='Seleccionar Rol'
    # )

    # filtro_usuarios_email = forms.ModelMultipleChoiceField(
    #     queryset=User.objects.all(),
    #     widget=forms.SelectMultiple(
    #         attrs={
    #             'class': 'form-control',
    #             'id': 'filtro-usuarios',  # Agregamos un id para controlarlo con JS
    #         }
    #     ),
    #     required=False,
    #     label='Seleccionar Usuarios'
    # )

    # def __init__(self, *args, **kwargs):
    #     super(FormEventosNotificacion, self).__init__(*args, **kwargs)
    #     # Inicialmente ocultamos ambos campos dependientes
    #     self.fields['filtro_rol'].widget.attrs['style'] = 'display:none;'
    #     self.fields['filtro_usuarios_email'].widget.attrs['style'] = 'display:none;'
    

    def __init__(self, *args, **kwargs):
        super(FormEventosNotificacion, self).__init__(*args, **kwargs)

        # Añadir la opción "Todos" y los roles
        self.fields['filtro_rol'].choices = [('todos', 'Todos los Roles')] + [
            (group.id, group.name) for group in Group.objects.all()
        ]

        # Añadir la opción "Todos" y los usuarios
        self.fields['filtro_usuarios_email'].choices = [('todos', 'Todos los Usuarios')] + [
            (user.id, user.email) for user in User.objects.all()
        ]

        # Inicialmente ocultamos ambos campos dependientes
        self.fields['filtro_rol'].widget.attrs['style'] = 'display:none;'
        self.fields['filtro_usuarios_email'].widget.attrs['style'] = 'display:none;'
        # self.fields['select_usuarios_por_correo_rol'].choices = [
        #     (user) for user in User.get_emails_agrouped_by_role()
        # ]


    # select_usuarios = forms.ModelChoiceField(
    #     queryset=super(), 
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-control',
    #         }
    #     ),
    # )

    # select_usuarios_por_correo_rol = forms.MultipleChoiceField(
    #     widget=forms.SelectMultiple(
    #         attrs={
    #             'class': 'form-control',
    #         }
    #     ),
    #     label='Seleccionar Usuarios o Roles',
    #     required=False
    # )
    
    # select_usuarios_por_correo_rol_agrupado = forms.MultipleChoiceField(
    #     widget=forms.SelectMultiple(
    #         attrs={
    #             'class': 'form-control',
    #         }
    #     ),
    #     label='Seleccionar Usuarios o Roles',
    #     required=False
    # )
    
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
        
        