from django.db import models
from dashboard.models.usuarios import User
class CorreosUsuarios(models.Model):
    nombre_usuario = models.CharField(max_length=30)
    correo = models.CharField(max_length=30)
    usuario_id = models.ForeignKey(User, on_delete=models.CASCADE )