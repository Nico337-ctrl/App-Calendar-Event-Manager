from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator

class User(AbstractUser):
        
    email = models.EmailField('Correo electrónico', max_length=250, unique=True)
    telefono = models.CharField(
        'Teléfono', 
        max_length=10, 
        validators=[RegexValidator(regex=r'^\d{10}$', message='El teléfono debe tener 10 dígitos.')]
    )
    imagen = models.ImageField(
        'Imagen de perfil', 
        upload_to='media/',
    ) 
    first_name = models.CharField('Nombre', max_length=50)
    last_name = models.CharField('Apellido', max_length=50)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, blank=True, related_name='roles')
    def __str__(self):
        return self.username
