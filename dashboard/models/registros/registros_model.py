from django.db import models
from django.contrib.auth.models import User
from .tipoRegistro_model import TipoRegistro
from dashboard.models.eventos import Eventos


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

