from django.dispatch import receiver
from django.db.models.signals import *
from dashboard.models.registros import EntidadRegistro


@receiver(post_migrate, sender=EntidadRegistro)
def crear_EntidadRegistro(sender, instance, **kwargs):
    EntidadRegistro.objects.create(
        nombre_entidad="Eventos",
    ),
    EntidadRegistro.objects.create(
        nombre_entidad="EtiquetaEventos",
    ),
    EntidadRegistro.objects.create(
        nombre_entidad="Usuarios",
    ),

    