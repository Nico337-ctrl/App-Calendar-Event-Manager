from django.dispatch import receiver
from django.db.models.signals import *
from dashboard.models.usuarios import User
from dashboard.models.registros import Registros, TipoRegistro, EntidadRegistro


@receiver(post_save, sender=User)
def registrar_evento(sender, instance, created, **kwargs):
    tipo_accion = 'CREACION' if created else 'ACTUALIZACION'
    tipo_registro = TipoRegistro.objects.get(accion=tipo_accion)
    usuario = instance  # Aquí debes usar la instancia de `User`, no el ID
    entidad, _ = EntidadRegistro.objects.get_or_create(
        nombre_entidad='Usuarios',
    )
    
    Registros.objects.create(
        tipo=tipo_registro,
        usuario=usuario,
        entidad=entidad,
        elemento_id=instance.id  # Asigna el ID del evento al campo elemento_id
    )

@receiver(post_delete, sender=User)
def registrar_evento_eliminado(sender, instance, **kwargs):
    tipo_registro = TipoRegistro.objects.get(accion='ELIMINAR')
    usuario = instance  # Aquí también debes usar la instancia de `User`
    entidad, _ = EntidadRegistro.objects.get_or_create(
        nombre_entidad='Usuarios',
    )
    
    Registros.objects.create(
        tipo=tipo_registro,
        usuario=usuario,
        entidad=entidad,
        elemento_id=instance.id  # Asigna el ID del evento al campo elemento_id
    )
    