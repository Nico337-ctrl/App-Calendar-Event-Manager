from django.db import models


class EtiquetaEvento(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    imagen = models.ImageField()



