from django.db import models
from dashboard.models.usuarios import User


class User_Perfil(models.Model):
    usuario_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='usuario_id')
    perfil_imagen = models.ImageField(
        'Imagen de perfil', 
        upload_to='media/',
        null=True
    )
    