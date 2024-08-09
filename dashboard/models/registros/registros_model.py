from django.db import models
from dashboard.models.usuarios import User
from .tipoRegistro_model import TipoRegistro
from .entidadRegistro_model import EntidadRegistro



class Registros(models.Model):
    tipo = models.ForeignKey(TipoRegistro, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT )
    entidad = models.ForeignKey(EntidadRegistro, on_delete=models.PROTECT)
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)





