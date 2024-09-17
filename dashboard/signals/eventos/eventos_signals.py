from django.dispatch import receiver
from django.db.models.signals import *
from dashboard.models.eventos import Eventos
from dashboard.models.registros import Registros, TipoRegistro, EntidadRegistro
from django.forms.models import model_to_dict
from datetime import datetime


def convert_datetime_fields(data):
    """Convierte los campos datetime en formato ISO string."""
    for field, value in data.items():
        if isinstance(value, datetime):
            data[field] = value.isoformat()  # Convertir a cadena en formato ISO 8601
    return data


@receiver(pre_save, sender=Eventos)
# Verificar una instancia anterior a la creada
def cache_old_instance(sender, instance, **kwargs):
    try:
        instance._old_instance = Eventos.objects.get(pk=instance.pk)
    except Eventos.DoesNotExist:
        instance._old_instance = None


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
        valor_nuevo = convert_datetime_fields(model_to_dict(instance))
        valor_nuevo_str = ', '.join(f'{key}: {value}' for key, value in valor_nuevo.items())
        Registros.objects.create(
            tipo=tipo_registro,
            usuario=usuario,
            entidad=entidad,
            elemento_id=instance.id,
            campo_modificado='Todos los campos',
            valor_anterior=None,
            valor_nuevo=valor_nuevo_str,
        )
    else:
        # Registrando la actualizacion del evento (model:Eventos)
        old_instance = getattr(instance, '_old_instance', None)
        if old_instance:
            old_data = convert_datetime_fields(model_to_dict(old_instance))
            new_data = convert_datetime_fields(model_to_dict(instance))

            campos_modificados = []
            valor_anterior = {}
            valor_nuevo = {}

            for field in old_data:
                if old_data[field] != new_data[field]:
                    campos_modificados.append(field)
                    valor_anterior[field] = old_data[field]
                    valor_nuevo[field] = new_data[field]
                    

            # valor_anterior_str = ', '.join(f'{key}: {value}' for key, value in valor_anterior.items())
            # valor_nuevo_str = ', '.join(f'{key}: {value}' for key, value in valor_nuevo.items())


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
    
    valor_anterior = convert_datetime_fields(model_to_dict(instance))
    Registros.objects.create(
        tipo=tipo_registro,
        usuario=usuario,
        entidad=entidad,
        elemento_id=instance.id,
        campo_modificado='Todos los campos',
        valor_anterior=valor_anterior,
        valor_nuevo=None,
    )
    