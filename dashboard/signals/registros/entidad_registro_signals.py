from django.dispatch import receiver
from django.db.models.signals import *
from dashboard.models.registros import EntidadRegistro

@receiver(post_migrate)
def crear_entidad_registro(sender, **kwargs):
    # Lista de entidades a crear
    entidades = [
        "Eventos",
        "EtiquetaEventos",
        "Usuarios",
    ]
    
    for nombre_entidad in entidades:
        EntidadRegistro.objects.get_or_create(
            nombre_entidad=nombre_entidad
        )
    