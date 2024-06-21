from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class evento_abstract(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class evento_miembro(evento_abstract):
    titulo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    comienza = models.DateTimeField()
    termina = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    


    

