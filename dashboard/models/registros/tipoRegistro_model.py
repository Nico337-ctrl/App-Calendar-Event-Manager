from django.db import models

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