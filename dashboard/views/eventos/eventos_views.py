from django.db.models.base import Model as Model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from dashboard.forms.eventos.eventos_forms import FormEventos
from dashboard.models.eventos import Eventos
from notifications.send_notification import enviarNotificacion
from django.contrib import messages

""" Aqui comienzan las vistas para el modulo de eventos """

class EventoIndex(LoginRequiredMixin, ListView):
    template_name= 'evento/evento_index.html'
    queryset = Eventos.objects.all()
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'eventos'



class EventoCreate(LoginRequiredMixin, CreateView):
    template_name = 'evento/evento_create.html'
    success_url = '/dashboard/evento/'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        context = {'formulario' : FormEventos }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            formulario = (request.POST)
            nuevo_evento = formulario.save(commit=False)
            nuevo_evento.user = request.user
            nuevo_evento.etiqueta = request
            nuevo_evento.save()

            enviarNotificacion(titulo='Haz credo un nuevo evento', 
                               mensaje=f'El evento {formulario.titulo}')
            

            return redirect(self.success_url)
        except ValueError as e:
            context = {'formulario' :  FormEventos}
            messages.error(request, f"Por favor ingrese datos validos. {str(e)}")
            return render(request, self.template_name, context)
            
            
class EventoDetail(LoginRequiredMixin, DetailView):
    template_name = 'evento/evento_detail.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = Eventos
    context_object_name = 'evento'
        
        

class EventoEdit(LoginRequiredMixin, UpdateView):
    template_name = 'evento/evento_edit.html'
    success_url = 'evento/evento_index.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = Eventos
    form_class =  FormEventos
    
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
        return redirect('/dashboard/evento/')


class EventoDelete(LoginRequiredMixin, DeleteView):
    template_name = 'evento/evento_index.html'
    success_url = 'evento/evento_index.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        evento = Eventos.objects.get(id = self.kwargs['pk'])
        evento.delete()
        return redirect('/dashboard/evento/')

""" Aqui termina las vistas para el modulo de eventos """