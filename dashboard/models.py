from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class EventoAbstract(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class EventoMiembro(EventoAbstract):
    titulo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    comienza = models.DateTimeField()
    termina = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    


    

