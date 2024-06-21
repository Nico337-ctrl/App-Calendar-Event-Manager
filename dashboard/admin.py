
from django.contrib import admin
from .models import evento_miembro

class AdminEvento(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'comienza', 'termina')

admin.site.register(evento_miembro, AdminEvento)
