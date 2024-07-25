from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class EtiquetaEvento(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    imagen = models.ImageField()

class Eventos(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    info_extra = models.CharField(max_length=255)
    inicia_el = models.DateTimeField()
    termina_el = models.DateTimeField()
    est_activo = models.BooleanField(default=True)
    est_desactivo = models.BooleanField(default=False)
    etiqueta = models.ForeignKey(EtiquetaEvento,on_delete=models.PROTECT, default=None )
    usuario = models.ForeignKey(User, on_delete=models.PROTECT )
    
    @property
    def nombre_tabla(self):
        return self._meta.db_table

class TipoRegistro(models.Model):
    ACCIONES = [
        ('CREACION', 'Creación'),
        ('ACTUALIZACION', 'Actualización'),
        ('ELIMINAR', 'Eliminar'),
        ('NINGUNA', 'Ninguna'),
    ]

    nombre_accion = models.CharField(
        max_length=15,
        choices=ACCIONES,
        default='NINGUNA',
    )
    
    def __str__(self):
        return self.nombre_accion

class Registros(models.Model):
    tipo = models.ForeignKey(TipoRegistro, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT )
    evento = models.ForeignKey(Eventos, on_delete=models.PROTECT)
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)
    tabla_origen = models.CharField(max_length=20, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.tabla_origen = Eventos._meta.db_table
        super().save(*args, **kwargs)

    


    

