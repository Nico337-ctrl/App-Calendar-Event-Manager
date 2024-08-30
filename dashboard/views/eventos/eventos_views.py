from django.db.models.base import Model as Model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import *
from dashboard.forms.eventos.eventos_forms import FormEventos
from dashboard.models.eventos import Eventos
from notifications.send_notification import notificacion
from dashboard.views.mixins import *


""" Aqui comienzan las vistas para el modulo de eventos """

class EventoIndex(LoginRequiredMixin, PermissionRequiredMixin, UserGroupContextMixin ,ListView):
    template_name= 'evento/evento_index.html'
    queryset = Eventos.objects.all()
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'eventos'
    permission_required = 'dashboard.view_eventos'
    

                

class EventoCreate(LoginRequiredMixin, PermissionRequiredMixin ,CreateView):
    template_name = 'evento/evento_create.html'
    success_url = '/dashboard/evento/'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    permission_required = 'dashboard.add_eventos'

    def get(self, request, *args, **kwargs):
        context = {'formulario' : FormEventos}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
            try:
                formulario = FormEventos(request.POST)
                if formulario.is_valid():
                    nuevo_evento = formulario.save(commit=False)
                    nuevo_evento.usuario = request.user
                    nuevo_evento.save()
                    notificacion(titulo='Nuevo Evento', 
                                mensaje=f'El evento {nuevo_evento.titulo} ha sido creada.')
                    
                    
                return redirect(self.success_url)
            except ValueError as e:
                context = {'formulario' :  FormEventos}
                messages.error(request, f"Por favor ingrese datos validos. {str(e)}")
                return render(request, self.template_name, context)
            
        
        




    # def correo(self, request, nuevo_evento):
    #     if nuevo_evento.notificar:
    #         if nuevo_evento.notificar_a == 'todos':
    #             usuarios = User.objects.all()
    #             agg = destinatarios.append(usuarios)
    #         elif nuevo_evento.notificar_a == 'roles':
    #             usuarios = User.objects.filter(groups__in=nuevo_evento.roles.all()).distinct()
    #             agg = destinatarios.append(usuarios)
    #         elif nuevo_evento.notificar_a == 'manual':
    #             usuarios = nuevo_evento.usuarios.all()
    #             agg = destinatarios.append(usuarios)
        
    #     destinatarios = []
    #     datos = {}
    #     datos.update({'Titulo': {nuevo_evento.titulo},
    #                   'Descripcion': {nuevo_evento.descripcion},
    #                   'Info Extra': {nuevo_evento.info_extra},
    #                   'Inicia el': {nuevo_evento.inicia_el},
    #                   'Termina_el': {nuevo_evento.termina_el},
    #                   'Estado:':{nuevo_evento.est_activo},
    #                   'Estado:':{nuevo_evento.etiqueta}
    #                   })
    #     enviar_correo(destinatarios, asusnto=nuevo_evento.titulo, tipo_correo=nuevo_evento.etiqueta, datos=datos )


            
            
class EventoDetail(LoginRequiredMixin, PermissionRequiredMixin ,DetailView):
    template_name = 'evento/evento_detail.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = Eventos
    context_object_name = 'evento'
    permission_required = 'dashboard.view_eventos'
        
        

class EventoEdit(LoginRequiredMixin, PermissionRequiredMixin ,UpdateView):
    template_name = 'evento/evento_edit.html'
    success_url = '/dashboard/evento/'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = Eventos
    form_class =  FormEventos
    permission_required = 'dashboard.change_eventos'
    
    def get(self, request, *args, **kwargs):
        evento = get_object_or_404(self.model, pk=self.kwargs['pk'])
        formulario = self.form_class(instance=evento)
        context = {'evento': evento, 'formulario': formulario}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        evento = get_object_or_404(self.model, pk=self.kwargs['pk'])
        formulario = self.form_class(request.POST, instance=evento)
        if formulario.is_valid():
            formulario.save()
            notificacion(titulo='Evento Modificado', 
                                mensaje=f'El evento {evento.titulo} ha sido actualizado. ')
        return redirect('/dashboard/evento/')


class EventoDelete(LoginRequiredMixin, PermissionRequiredMixin ,DeleteView):
    template_name = 'evento/evento_index.html'
    success_url = 'evento/evento_index.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    permission_required = 'dashboard.delete_eventos'

    def get(self, request, *args, **kwargs):
        evento = Eventos.objects.get(id = self.kwargs['pk'])
        evento.delete()
        notificacion(titulo='Evento Eliminado', 
                                mensaje=f'El evento {evento.titulo} ha sido eliminado. ')
        return redirect('/dashboard/evento/')
    
    


""" Aqui termina las vistas para el modulo de eventos """