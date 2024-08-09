from django.dispatch import receiver
from django.db.models.signals import *
from dashboard.models.eventos import Eventos
from dashboard.models.registros import Registros, TipoRegistro, EntidadRegistro


@receiver(post_save, sender=Eventos)
def registrar_evento(sender, instance, created, **kwargs):
    tipo_accion = 'CREACION' if created else 'ACTUALIZACION'
    tipo_registro = TipoRegistro.objects.get(accion=tipo_accion)
    usuario = instance.usuario  # Asumiendo que `usuario` es un campo de ForeignKey en `Eventos`
    entidad, _ = EntidadRegistro.objects.get_or_create(
        nombre_entidad='Eventos',
    )
    
    Registros.objects.create(
        tipo=tipo_registro,
        usuario=usuario,
        entidad=entidad
    )
    
@receiver(post_delete, sender=Eventos)
def registrar_evento_eliminado(sender, instance, **kwargs):
    tipo_registro = TipoRegistro.objects.get(accion='ELIMINAR')
    usuario = instance.usuario  # Asumiendo que `usuario` es un campo de ForeignKey en `Eventos`
    entidad, _ = EntidadRegistro.objects.get_or_create(
        nombre_entidad='Eventos',
    )
    
    Registros.objects.create(
        tipo=tipo_registro,
        usuario=usuario,
        entidad=entidad
    )
    