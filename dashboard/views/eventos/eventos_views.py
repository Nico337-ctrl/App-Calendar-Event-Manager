from django.db.models.base import Model as Model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import *
from dashboard.forms.eventos.eventos_forms import FormEventos
from dashboard.forms.eventos.eventos_notificaciones_forms import FormEventosNotificacion
from dashboard.models.eventos import Eventos
from dashboard.models.usuarios import User
from notifications.send_notification import notificacion
from dashboard.views.mixins import *
from django.contrib import messages
from notifications.emails.send_email import enviar_correo


""" Aqui comienzan las vistas para el modulo de eventos """

class EventoIndex(LoginRequiredMixin, ValidarPermisosRequeridosMixin, UserGroupContextMixin ,ListView):
    template_name= 'evento/evento_index.html'
    queryset = Eventos.objects.all()
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'eventos'
    permission_required = 'dashboard.view_eventos'
    

                

class EventoCreate(LoginRequiredMixin, ValidarPermisosRequeridosMixin, UserGroupContextMixin ,CreateView):
    template_name = 'evento/evento_create.html'
    success_url = '/dashboard/evento/'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    permission_required = 'dashboard.add_eventos'

    

    def get(self, request, *args, **kwargs):
        context = {'formulario' : FormEventos, 'form_notificar': FormEventosNotificacion }
        context.update(self.get_user_group_context())
        return render(request, self.template_name, context)
        
    def post(self, request, *args, **kwargs):
            try:
                form_notificar = FormEventosNotificacion(request.POST)
                formulario = FormEventos(request.POST)
                
                if formulario.is_valid() and form_notificar.is_valid():
                    """Guardar datos del evento"""
                    nuevo_evento = formulario.save(commit=False)
                    nuevo_evento.usuario = request.user
                    nuevo_evento.save()

                    """Obtener usuarios a notificar"""
                    usuarios = self.obtener_usuarios_notificacion(form_notificar)

                    """Enviar correos a los usuarios"""
                    self.correo(nuevo_evento, usuarios)

                    """Enviar notificación"""
                    notificacion(
                        titulo='Nuevo Evento', 
                        mensaje=f'El evento {nuevo_evento.titulo} ha sido creado.'
                    )
                
                return redirect(self.success_url)

            except ValueError as e:
                context = {'formulario': FormEventos}
                messages.error(request, f"Por favor ingrese datos válidos. {str(e)}")
                return render(request, self.template_name, context)
        
    def obtener_usuarios_notificacion(self, form_notificar):
        filtro = form_notificar.cleaned_data['filtro']
        if filtro == 'rol_agrupado':
            rol = form_notificar.cleaned_data['filtro_rol']
            if rol == 'todos':
                usuarios = User.objects.all()  # Todos los usuarios
            else:
                usuarios = User.objects.filter(groups__id=rol)
            
        elif filtro == 'usuarios':
            usuarios_ids = form_notificar.cleaned_data['filtro_usuarios_email']
            if 'todos' in usuarios_ids:
                usuarios = User.objects.all()  # Todos los usuarios
            else:
                usuarios = User.objects.filter(id__in=usuarios_ids)

        return usuarios

    """Función para el envío de correos"""
    def correo(self, evento, usuarios):
            destinatarios = [usuario.email for usuario in usuarios if usuario.email]

            datos = {
                'Titulo': evento.titulo,
                'Descripcion': evento.descripcion,
                'Info_Extra': evento.info_extra,
                'Inicia_el': evento.inicia_el,
                'Termina_el': evento.termina_el,
                'Estado': evento.est_activo,
                'Etiqueta': evento.etiqueta,
            }

            """Lógica para enviar el correo"""
            enviar_correo(destinatarios=destinatarios, asunto=evento.titulo,  datos=datos)
                
            
class EventoDetail(LoginRequiredMixin, ValidarPermisosRequeridosMixin, UserGroupContextMixin ,DetailView):
    template_name = 'evento/evento_detail.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = Eventos
    context_object_name = 'evento'
    permission_required = 'dashboard.view_eventos'
        
        

class EventoEdit(LoginRequiredMixin, ValidarPermisosRequeridosMixin , UserGroupContextMixin ,UpdateView):
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


class EventoDelete(LoginRequiredMixin, ValidarPermisosRequeridosMixin , UserGroupContextMixin ,DeleteView):
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