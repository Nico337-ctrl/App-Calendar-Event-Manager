from django.db.models.base import Model as Model
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import *
from dashboard.forms.users import *
from dashboard.models.usuarios import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from dashboard.views.mixins import *


""" Aqui comienzan las vistas para el modulo de usuarios"""

class UsuarioIndex(LoginRequiredMixin, ValidarPermisosRequeridosMixin, UserGroupContextMixin, View):
    template_name = 'usuario/usuario_index.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'usuarios'
    permission_required = 'dashboard.view_user'

    def get(self, request, *args, **kwargs):
        
        logged_in_user = request.user
        queryset = User.objects.exclude(id=logged_in_user.id)
        context = {
            'usuarios': queryset
        }
        context.update(self.get_user_group_context())
        return render(request, self.template_name, context)

class UsuarioCreate(LoginRequiredMixin, ValidarPermisosRequeridosMixin, UserGroupContextMixin ,CreateView):
    template_name = 'usuario/usuario_create.html'
    success_url = '/dashboard/usuario/'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    permission_required = 'dashboard.add_user'

    def get(self, request, *args, **kwargs):
        context = {'formulario': User_CreationForm()}
        context.update(self.get_user_group_context())
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        formulario = User_CreationForm(request.POST)
        if formulario.is_valid():
            try:
                nuevo_usuario = formulario.save(commit=False)
                nuevo_usuario.save()
                selected_group = formulario.cleaned_data.get('group')
                if selected_group:
                    nuevo_usuario.groups.add(selected_group)
                # enviarNotificacion()
                return redirect(self.success_url)
            except Exception as e:
                messages.error(request, f"Error al guardar el usuario: {e}")
        else:
            for field, errors in formulario.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
        context = {'formulario': formulario}
        return render(request, self.template_name, context)


class UsuarioDetail(LoginRequiredMixin, ValidarPermisosRequeridosMixin , UserGroupContextMixin, DetailView):
    template_name = 'usuario/usuario_detail.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = User
    context_object_name = 'usuario'
    permission_required = 'dashboard.detailview_user'


class UsuarioEdit(LoginRequiredMixin, ValidarPermisosRequeridosMixin, UserGroupContextMixin, UpdateView):
    template_name = 'usuario/usuario_edit.html'
    success_url = '/dashboard/usuario/'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = User
    form_class = User_ChangeForm
    permission_required = 'dashboard.change_user'
    
    def get_success_url(self):
        return reverse('usuario')

    def get(self, request, *args, **kwargs):
        usuario = get_object_or_404(self.model, pk=self.kwargs['pk'])
        formulario = self.form_class(instance=usuario)
        context = {'usuario': usuario, 'formulario': formulario}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        usuario = get_object_or_404(self.model, pk=self.kwargs['pk'])
        formulario = self.form_class(request.POST, request.FILES, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            return redirect(self.get_success_url())
        else:
            for field, errors in formulario.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
            # Opcional: puedes agregar un mensaje de error aquí
            context = {'usuario': usuario, 'formulario': formulario}
            
            return render(request, self.template_name, context)

class UsuarioDelete(LoginRequiredMixin, ValidarPermisosRequeridosMixin, UserGroupContextMixin, DeleteView):
    # template_name = 'usuario/evento_edit.html'
    success_url = 'usuario/usuario_index.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    permission_required = 'dashboard.delete_user'
    
    def get(self, request, *args, **kwargs):
        usuario = User.objects.get(id = self.kwargs['pk'])
        usuario.delete()
        return redirect('/dashboard/usuario/')

class UsuarioChangePassword(LoginRequiredMixin, ValidarPermisosRequeridosMixin, UserGroupContextMixin, View):
    model = User
    template_name = 'usuario/usuario_changePassword.html'
    success_url = '/dashboard/usuario/'
    permission_required = 'dashboard.change_user'

    def get(self, request, *args, **kwargs):
        usuario = get_object_or_404(self.model, pk=self.kwargs['pk'])
        formulario = user_PasswordChangeForm(user=request.user)
        context = {'usuario': usuario, 'formulario': formulario}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        usuario = get_object_or_404(self.model, pk=self.kwargs['pk'])
        formulario = user_PasswordChangeForm(user=request.user, data=request.POST)
        context = { 'usuario': usuario, 'formulario': formulario}
        try:
            if formulario.is_valid():
                user = formulario.save()
                update_session_auth_hash(request, user)
                messages.success(request, '¡Tu contraseña ha sido cambiada exitosamente!')
                return redirect(self.success_url)
            else:
                for field, errors in formulario.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado: {str(e)}")
        
        return render(request, self.template_name, context)
    
    
class UsuarioProfile(UserGroupContextMixin, ListView):
    template_name = 'usuario/perfil_usuario.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = User
    context_object_name = 'usuario'

""" Aqui terminan las vistas para el modulo usuarios """
