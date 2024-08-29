
from django.contrib import admin
from dashboard.models import Eventos, User

class AdminUsuarios(admin.ModelAdmin):
    list_display = ('id', 'username', 'password' ,'first_name', 'last_name', 'email', 'telefono', 'groups_list')
    def groups_list(self, obj):
        return ", ".join(group.name for group in obj.groups.all())
    groups_list.short_description = 'Groups'  

admin.site.register(User, AdminUsuarios)

class AdminEventos(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'info_extra', 'inicia_el', 'termina_el')

admin.site.register(Eventos, AdminEventos)
