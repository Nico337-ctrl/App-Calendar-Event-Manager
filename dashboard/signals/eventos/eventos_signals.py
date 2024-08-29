from django.dispatch import receiver
from django.db.models.signals import *
from dashboard.models.eventos import Eventos
from dashboard.models.registros import Registros, TipoRegistro, EntidadRegistro
from django.forms.models import model_to_dict

@receiver(post_save, sender=Eventos)
def registrar_evento(sender, instance, created, **kwargs):
    tipo_accion = 'CREACION' if created else 'ACTUALIZACION'
    tipo_registro = TipoRegistro.objects.get(accion=tipo_accion)
    usuario = instance.usuario  # Asumiendo que `usuario` es un campo de ForeignKey en `Eventos`
    entidad, _ = EntidadRegistro.objects.get_or_create(
        nombre_entidad='Eventos',
    )
    
    if created:
        # Registra la creación del evento
        Registros.objects.create(
            tipo=tipo_registro,
            usuario=usuario,
            entidad=entidad,
            elemento_id=instance.id,
            campo_modificado='Todos los campos',
            valor_anterior=None,
            valor_nuevo=model_to_dict(instance),
        )
    else:
        # Registra la actualización del evento
        try:
            old_instance = Eventos.objects.get(pk=instance.pk)
        except Eventos.DoesNotExist:
            old_instance = None

        if old_instance:
            old_data = model_to_dict(old_instance)
            new_data = model_to_dict(instance)
            for field in old_data:
                if old_data[field] != new_data[field]:
                    Registros.objects.create(
                        tipo=tipo_registro,
                        usuario=usuario,
                        entidad=entidad,
                        elemento_id=instance.id,
                        campo_modificado=field,
                        valor_anterior=old_data[field],
                        valor_nuevo=new_data[field],
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
        entidad=entidad,
        elemento_id=instance.id,
        campo_modificado='Todos los campos',
        valor_anterior=model_to_dict(instance),
        valor_nuevo=None,
    )
    