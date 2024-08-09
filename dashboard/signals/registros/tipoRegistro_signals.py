from django.dispatch import receiver
from django.db.models.signals import *
from dashboard.models.registros import TipoRegistro


@receiver(post_migrate, sender=TipoRegistro)
def crear_tipoRegistro(sender, instance, **kwargs):
    TipoRegistro.objects.create(
        accion="CREACION",
        descripcion="Creación",
    ),
    TipoRegistro.objects.create(
        accion="ACTUALIZACION",
        descripcion="Actualización",
    ),
    TipoRegistro.objects.create(
        accion="ELIMINAR",
        descripcion="Eliminar",
    )
    