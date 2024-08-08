from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator

class User(AbstractUser):
        
    email = models.EmailField('Correo electrónico', max_length=250, unique=True)
    telefono = models.CharField(
        'Teléfono', 
        max_length=10, 
        blank=True, 
        null=True, 
        validators=[RegexValidator(regex=r'^\d{10}$', message='El teléfono debe tener 10 dígitos.')]
    )
    imagen = models.ImageField(
        'Imagen de perfil', 
        upload_to='images/',
    )
    first_name = models.CharField('Nombre', max_length=50)
    last_name = models.CharField('Apellido', max_length=50)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set', 
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  
        blank=True
    )

    def __str__(self):
        return self.username
