from django.dispatch import receiver
from django.db.models.signals import *
from dashboard.models.usuarios import User
from dashboard.models.usuarios import User_Perfil

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    usuario_id = instance  # Aquí debes usar la instancia de `User`, no el ID
    
    if created:
        # Registra la creación del evento
        User_Perfil.objects.create(
            perfil_imagen=None,
            usuario_id= usuario_id
        )
