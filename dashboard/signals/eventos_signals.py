from django.dispatch import receiver
from django.db.models.signals import *
from dashboard.models.eventos import Eventos
from dashboard.models.registros import Registros, EntidadRegistro, TipoRegistro


@receiver(post_save, sender=Eventos)
def registrar_evento_guardado(sender, instance, created, **kwargs):
    if created:
        tipo_accion = TipoRegistro.objects.get(nombre_accion='CREACION')
    else:
        tipo_accion = TipoRegistro.objects.get(nombre_accion='ACTUALIZACION')
    
    entidad = EntidadRegistro.objects.create(
        nombre_entidad=instance.nombre_tabla,
        elemento_id=instance.id
    )
    
    Registros.objects.create(
        tipo=tipo_accion,
        usuario=instance.usuario,
        entidad=entidad,
        creado_el=instance.creado_el,
        actualizado_el=instance.actualizado_el
    )

# Signal para eliminación
@receiver(post_delete, sender=Eventos)
def registrar_evento_eliminado(sender, instance, **kwargs):
    tipo_accion = TipoRegistro.objects.get(nombre_accion='ELIMINAR')
    
    entidad = EntidadRegistro.objects.create(
        nombre_entidad=instance.nombre_tabla,
        elemento_id=instance.id
    )
    
    Registros.objects.create(
        tipo=tipo_accion,
        usuario=instance.usuario,
        entidad=entidad,
        creado_el=instance.creado_el,
        actualizado_el=instance.actualizado_el
    )
