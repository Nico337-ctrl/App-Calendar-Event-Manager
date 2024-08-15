from django.db import models
from dashboard.models.usuarios import User
from .tipoRegistro_model import TipoRegistro
from .entidadRegistro_model import EntidadRegistro



class Registros(models.Model):
    tipo = models.ForeignKey(TipoRegistro, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    entidad = models.ForeignKey(EntidadRegistro, on_delete=models.PROTECT)
    elemento_id = models.PositiveIntegerField()
    campo_modificado = models.CharField(max_length=255)
    valor_anterior = models.TextField(null=True, blank=True)
    valor_nuevo = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.entidad} - {self.elemento_id}"





