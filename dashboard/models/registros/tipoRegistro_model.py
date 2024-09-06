from django.db import models

class TipoRegistro(models.Model):
    accion = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    
    def __str__(self):
        return self.accion

