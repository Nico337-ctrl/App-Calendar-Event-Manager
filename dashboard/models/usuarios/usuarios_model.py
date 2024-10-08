from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.db.models import Prefetch

class User(AbstractUser):
        
    email = models.EmailField('Correo electrónico', max_length=250, unique=True)
    telefono = models.CharField(
        'Teléfono', 
        max_length=10, 
        validators=[RegexValidator(regex=r'^\d{10}$', message='El teléfono debe tener 10 dígitos.')]
    )
    first_name = models.CharField('Nombre', max_length=50)
    last_name = models.CharField('Apellido', max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name='roles')


    def __str__(self):
        return self.username


    
    @classmethod
    def filtrar_correos(cls):
        return cls.objects.values_list('email', flat=True)
    """
    Metodo para poder filtrar todos los correos de los usuarios.
    """

    @classmethod
    def filtrar_correos_por_rol(rol_nombre):
        return User.objects.filter(group__name=rol_nombre).values_list('email', flat=True)
    """
    Metodo para filtrar todos los correos de los usuarios por su rol.
    """

    @classmethod
    def filtrar_correos_por_rol_agrupado():
        roles = Group.objects.prefetch_related(
            Prefetch('roles', queryset=User.objects.values_list('email', flat=True))
        )
        return {role.name: list(role.roles.values_list('email', flat=True)) for role in roles}
    """
    Metodo para filtrar todos los correos de los usuarios por su rol de manera agrupada.
    """
