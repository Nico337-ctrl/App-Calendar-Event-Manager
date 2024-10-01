from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from dashboard.models import User

@receiver(post_migrate)
def create_roles_and_permissions(sender, **kwargs):
    # Definir los roles y permisos
    roles = {
        'Administrador': 'all',
        'Colaborador': [
            'add_etiquetaevento', 'change_etiquetaevento', 'delete_etiquetaevento', 'view_etiquetaevento',
            'add_eventos', 'change_eventos', 'delete_eventos', 'view_eventos',
            'view_registros',
            'view_user',
        ],
        'Asistente': ['view_eventos']
    }
    
    # Iterar sobre los roles y permisos
    for role_name, perm_codenames in roles.items():
        group, created = Group.objects.get_or_create(name=role_name)
        
        if perm_codenames == 'all':
            all_permissions = Permission.objects.all()
            group.permissions.set(all_permissions)
        else:
            permissions = Permission.objects.filter(codename__in=perm_codenames)
            group.permissions.set(permissions)
            
@receiver(post_migrate)
def create_default_user(sender, **kwargs):
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(
                username='admin', 
                password='admin123456', 
                email='admin@gmail.com', 
                telefono= '3569875631', 
                first_name= 'admin', 
                last_name='admin',
                group_id = 1)