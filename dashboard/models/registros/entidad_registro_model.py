from django.db import models



class EntidadRegistro(models.Model):
    nombre_entidad = models.CharField(max_length=50)
    

