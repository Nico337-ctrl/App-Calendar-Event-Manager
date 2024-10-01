from django.dispatch import receiver
from django.db.models.signals import *
from dashboard.models.registros import TipoRegistro


@receiver(post_migrate)
def crear_tipo_registro(sender, **kwargs):
    # Lista de acciones a crear
    acciones = [
        {"accion": "CREACION", "descripcion": "Creación"},
        {"accion": "ACTUALIZACION", "descripcion": "Actualización"},
        {"accion": "ELIMINAR", "descripcion": "Eliminar"},
    ]
    
    for accion in acciones:
        TipoRegistro.objects.get_or_create(
            accion=accion["accion"],
            defaults={"descripcion": accion["descripcion"]}
        )