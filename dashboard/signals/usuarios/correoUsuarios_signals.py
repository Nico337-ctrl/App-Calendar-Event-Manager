from django.dispatch import receiver
from django.db.models.signals import *
from dashboard.models.usuarios import User
from dashboard.models.usuarios import CorreosUsuarios

@receiver(post_save, sender=User)
def guardar_correo(sender, instance, created, **kwargs):
    nombre_usuario = instance.username
    correo = instance.email
    usuario_id = instance  # Aquí debes usar la instancia de `User`, no el ID
    
    if created:
        # Registra la creación del evento
        CorreosUsuarios.objects.create(
            nombre_usuario=nombre_usuario,
            correo = correo, 
            usuario_id=usuario_id,
        )

