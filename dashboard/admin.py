
from django.contrib import admin
from .models import Eventos

class AdminEventos(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'info_extra', 'inicia_el', 'termina_el')

admin.site.register(Eventos, AdminEventos)
