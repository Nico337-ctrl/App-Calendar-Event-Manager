from django.dispatch import receiver
from django.db.models.signals import *
from dashboard.models.eventos import EtiquetaEvento
from dashboard.models.registros import Registros, TipoRegistro, EntidadRegistro
from django.forms.models import model_to_dict
from django.core.files import File
from datetime import datetime


def convert_datetime_fields(data):
    """Convierte los campos datetime en formato ISO string."""
    for field, value in data.items():
        if isinstance(value, datetime):
            data[field] = value.isoformat()  # Convertir a cadena en formato ISO 8601
    return data

def convert_image_fields(data):
    """Convierte los campos de imagen en URLs o nombres de archivo."""
    for field, value in data.items():
        if isinstance(value, File):  # Verifica si el campo es un archivo
            data[field] = value.url if hasattr(value, 'url') else value.name
    return data

def convert_fields(data):
    """Convierte tanto los campos datetime como los de imagen."""
    data = convert_datetime_fields(data)  # Convierte los datetime
    data = convert_image_fields(data)     # Convierte las imágenes
    return data

@receiver(pre_save, sender=EtiquetaEvento)
# Verificar una instancia anterior a la creada
def cache_old_instance(sender, instance, **kwargs):
    try:
        instance._old_instance = EtiquetaEvento.objects.get(pk=instance.pk)
    except EtiquetaEvento.DoesNotExist:
        instance._old_instance = None

@receiver(post_save, sender=EtiquetaEvento)
def registrar_etiqueta(sender, instance, created, **kwargs):
    tipo_accion = 'CREACION' if created else 'ACTUALIZACION'
    tipo_registro = TipoRegistro.objects.get(accion=tipo_accion)
    usuario = instance.usuario  # Asumiendo que `usuario` es un campo de ForeignKey en `EtiquetaEvento`
    entidad, _ = EntidadRegistro.objects.get_or_create(
        nombre_entidad='EtiquetaEventos',
    )
    
    if created:
        # Registra la creación del evento
        valor_nuevo = convert_fields(model_to_dict(instance))
        Registros.objects.create(
            tipo=tipo_registro,
            usuario=usuario,
            entidad=entidad,
            elemento_id=instance.id,
            campo_modificado='Todos los campos',
            valor_anterior=None,
            valor_nuevo=valor_nuevo,
        )
    else:
        # Registrando la actualizacion de la etiqueta (model:EtiquetaEvento)
        old_instance = getattr(instance, '_old_instance', None)
        if old_instance:
            old_data = convert_fields(model_to_dict(old_instance))
            new_data = convert_fields(model_to_dict(instance))

            campos_modificados = []
            valor_anterior = {}
            valor_nuevo = {}

            for field in old_data:
                if old_data[field] != new_data[field]:
                    campos_modificados.append(field)
                    valor_anterior[field] = old_data[field]
                    valor_nuevo[field] = new_data[field]

            for field in old_data:
                if old_data[field] != new_data[field]:
                    Registros.objects.create(
                        tipo=tipo_registro,
                        usuario=usuario,
                        entidad=entidad,
                        elemento_id=instance.id,
                        campo_modificado=', '.join(campos_modificados),
                        valor_anterior=old_data[field],
                        valor_nuevo=new_data[field],
                    )

@receiver(post_delete, sender=EtiquetaEvento)
def registrar_etiqueta_eliminada(sender, instance, **kwargs):
    tipo_registro = TipoRegistro.objects.get(accion='ELIMINAR')
    usuario = instance.usuario  # Asumiendo que `usuario` es un campo de ForeignKey en `EtiquetaEvento`
    entidad, _ = EntidadRegistro.objects.get_or_create(
        nombre_entidad='EtiquetaEventos',
    )
    
    valor_anterior = convert_fields(model_to_dict(instance))
    Registros.objects.create(
        tipo=tipo_registro,
        usuario=usuario,
        entidad=entidad,
        elemento_id=instance.id,
        campo_modificado='Todos los campos',
        valor_anterior=valor_anterior,
        valor_nuevo=None,
    )
    