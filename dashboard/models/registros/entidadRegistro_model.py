from django.db import models



class EntidadRegistro(models.Model):
    nombre_entidad = models.CharField(max_length=10)
    elemento_id = models.IntegerField()

