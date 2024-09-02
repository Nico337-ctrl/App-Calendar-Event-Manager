from django.db import models
from dashboard.models.usuarios import User


from .etiquetaEvento_model import EtiquetaEvento


class Eventos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    info_extra = models.CharField(max_length=255)
    inicia_el = models.DateTimeField()
    termina_el = models.DateTimeField()
    est_activo = models.BooleanField(default=True)
    notificar = models.BooleanField(default=True)
    etiqueta = models.ForeignKey(EtiquetaEvento,on_delete=models.CASCADE)
    
    @property
    def nombre_tabla(self):
        return self._meta.db_table