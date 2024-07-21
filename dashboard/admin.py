
from django.contrib import admin
from .models import EventoMiembro

class AdminEvento(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'comienza', 'termina')

admin.site.register(EventoMiembro, AdminEvento)
