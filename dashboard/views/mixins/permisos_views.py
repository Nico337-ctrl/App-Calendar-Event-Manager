from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse

class UserGroupContextMixin:
    def get_user_group_context(self):
        user = self.request.user
        context = {
            'is_admin': user.groups.filter(name='Administrador').exists(),
            'is_collaborator': user.groups.filter(name='Colaborador').exists(),
            'is_assistant': user.groups.filter(name='Asistente').exists(),
        }
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_group_context())
        return context
        

class ValidarPermisosRequeridosMixin(object):
    permission_required = ''
    url_redirect = None
    
    def get_perms(self):
        if isinstance(self.permission_required,str):
            return (self.permission_required,)
        else:
            return self.permission_required
    
    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse('home')
        return self.url_redirect
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect(self.get_url_redirect())