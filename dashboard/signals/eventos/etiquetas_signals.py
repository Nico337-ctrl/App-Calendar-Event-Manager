from django.dispatch import receiver
from django.db.models.signals import *
from dashboard.models.eventos import EtiquetaEvento
from dashboard.models.registros import Registros, TipoRegistro, EntidadRegistro


@receiver(post_save, sender=EtiquetaEvento)
def registrar_etiqueta(sender, instance, created, **kwargs):
    tipo_accion = 'CREACION' if created else 'ACTUALIZACION'
    tipo_registro = TipoRegistro.objects.get(accion=tipo_accion)
    usuario = instance.usuario  # Asumiendo que `usuario` es un campo de ForeignKey en `EtiquetaEvento`
    entidad, _ = EntidadRegistro.objects.get_or_create(
        nombre_entidad='EtiquetaEventos',
    )
    
    Registros.objects.create(
        tipo=tipo_registro,
        usuario=usuario,
        entidad=entidad,
        elemento_id=instance.id  # Asigna el ID del evento al campo elemento_id
    )

@receiver(post_delete, sender=EtiquetaEvento)
def registrar_etiqueta_eliminada(sender, instance, **kwargs):
    tipo_registro = TipoRegistro.objects.get(accion='ELIMINAR')
    usuario = instance.usuario  # Asumiendo que `usuario` es un campo de ForeignKey en `EtiquetaEvento`
    entidad, _ = EntidadRegistro.objects.get_or_create(
        nombre_entidad='EtiquetaEventos',
    )
    
    Registros.objects.create(
        tipo=tipo_registro,
        usuario=usuario,
        entidad=entidad,
        elemento_id=instance.id  # Asigna el ID del evento al campo elemento_id
    )
    