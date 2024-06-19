from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class eventoAbstract(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class eventoMiembro(eventoAbstract):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="eventos")
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    comienza = models.DateTimeField()
    termina = models.DateTimeField()

    


    

