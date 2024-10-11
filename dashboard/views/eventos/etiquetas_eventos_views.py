from django.db.models.base import Model as Model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import *
from dashboard.forms.eventos.etiqueta_eventos_forms import EtiquetaEventoForm
from dashboard.models.eventos import EtiquetaEvento
from notifications.send_notification import notificacion
from django.contrib import messages
from dashboard.views.mixins import *

""" Aqui comienzan las vistas para el modulo de etiquetas eventos """

class EventoEtiquetaIndex(LoginRequiredMixin, ValidarPermisosRequeridosMixin, UserGroupContextMixin ,ListView):
    template_name= 'evento/etiqueta/evento_etiqueta_index.html'
    queryset = EtiquetaEvento.objects.all()
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'etiquetas'
    permission_required = 'dashboard.view_etiquetaevento'


class EventoEtiquetaCreate(LoginRequiredMixin, ValidarPermisosRequeridosMixin, UserGroupContextMixin ,CreateView):
    template_name = 'evento/etiqueta/evento_etiqueta_create.html'
    success_url = '/dashboard/evento/etiqueta/'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    permission_required = 'dashboard.add_etiquetaevento'

    def get(self, request, *args, **kwargs):
        context = {'formulario' : EtiquetaEventoForm}
        context.update(self.get_user_group_context())
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            formulario = EtiquetaEventoForm(request.POST, request.FILES)
            if formulario.is_valid():
                nueva_etiqueta = formulario.save(commit=False)
                nueva_etiqueta.usuario = request.user
                nueva_etiqueta.save()

                notificacion(titulo='Nueva Etiqueta', 
                                mensaje=f'La etiqueta {nueva_etiqueta.titulo} ha sido creada.')
            
            return redirect(self.success_url)
        except ValueError as e:
            context = {'formulario' : EtiquetaEventoForm}
            messages.error(request, f"Por favor ingrese datos validos. {str(e)}")
            return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['is_admin_or_collaborator'] = ( user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Colaborador').exists() )
        context['is_assistant'] =  ( user.groups.filter(name='Asistente').exists() )
        
        return context
            
class EventoEtiquetaDetail(LoginRequiredMixin, ValidarPermisosRequeridosMixin,DetailView):
    template_name = 'evento/etiqueta/evento_etiqueta_detail.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = EtiquetaEvento
    context_object_name = 'etiqueta'
    permission_required = 'dashboard.detailview_etiquetaevento'
        
        

class EventoEtiquetaEdit(LoginRequiredMixin, ValidarPermisosRequeridosMixin,UpdateView):
    template_name = 'evento/etiqueta/evento_etiqueta_edit.html'
    success_url = 'evento/etiqueta/etiqueta_index.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = EtiquetaEvento
    form_class = EtiquetaEventoForm
    permission_required = 'dashboard.change_etiquetaevento'
    
    def get(self, request, *args, **kwargs):
        etiquetaEvento = get_object_or_404(self.model, pk=self.kwargs['pk'])
        formulario = self.form_class(instance=etiquetaEvento)
        context = {'etiqueta': etiquetaEvento, 'formulario': formulario}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        etiquetaEvento = get_object_or_404(self.model, pk=self.kwargs['pk'])
        formulario = self.form_class(request.POST, instance=etiquetaEvento)
        if formulario.is_valid():
            formulario.save()
            notificacion(titulo='Etiqueta Modificada', 
                                mensaje=f'La Etiqueta {etiquetaEvento.titulo} ha sido actualizada.')
        return redirect('/dashboard/evento/etiqueta/')


class EventoEtiquetaDelete(LoginRequiredMixin, ValidarPermisosRequeridosMixin,DeleteView):
    template_name = 'evento/etiqueta/evento_etiqueta_index.html'
    success_url = 'evento/etiqueta/etiqueta_index.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    permission_required = 'dashboard.delete_etiquetaevento'

    def get(self, request, *args, **kwargs):
        etiquetaEvento = EtiquetaEvento.objects.get(id = self.kwargs['pk'])
        etiquetaEvento.delete()
        notificacion(titulo='Etiqueta Eliminada', 
                                mensaje=f'La Etiqueta {etiquetaEvento.titulo} ha sido eliminada. ')
        return redirect('/dashboard/evento/etiqueta/')


""" Aqui termina las vistas para el modulo de etiquetas de eventos """
