
from django.contrib import admin
from .models import eventoMiembro

class AdminEvento(admin.ModelAdmin):
    list_display = ('usuario', 'titulo', 'descripcion', 'comienza', 'termina')

admin.site.register(eventoMiembro, AdminEvento)
