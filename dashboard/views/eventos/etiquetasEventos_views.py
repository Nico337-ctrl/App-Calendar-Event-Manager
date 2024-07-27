from django.db.models.base import Model as Model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from dashboard.forms.eventos.etiquetaEventos_forms import EtiquetaEventoForm
from dashboard.models.eventos import EtiquetaEvento
from notifications.send_notification import enviarNotificacion
from django.contrib import messages

""" Aqui comienzan las vistas para el modulo de etiquetas eventos """

class EventoEtiquetaIndex(LoginRequiredMixin, ListView):
    template_name= 'evento/etiqueta/etiqueta_index.html'
    queryset = EtiquetaEvento.objects.all()
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'etiquetas'



class EventoEtiquetaCreate(LoginRequiredMixin, CreateView):
    template_name = 'evento/etiqueta/etiqueta_create.html'
    success_url = '/dashboard/evento/etiqueta/'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        context = {'formulario' : EtiquetaEventoForm}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            formulario = EtiquetaEventoForm(request.POST)
            nueva_etiqueta = formulario.save(commit=False)
            nueva_etiqueta.save()

            enviarNotificacion(titulo='Haz credo una nueva etiqueta', 
                               mensaje=f'El evento {formulario.titulo}')
            
            return redirect(self.success_url)
        except ValueError as e:
            context = {'formulario' : EtiquetaEventoForm}
            messages.error(request, f"Por favor ingrese datos validos. {str(e)}")
            return render(request, self.template_name, context)
            
            
class EventoEtiquetaDetail(LoginRequiredMixin, DetailView):
    template_name = 'evento/etiqueta/etiqueta_detail.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = EtiquetaEvento
    context_object_name = 'etiqueta'
        
        

class EventoEtiquetaEdit(LoginRequiredMixin, UpdateView):
    template_name = 'evento/etiqueta/etiqueta_edit.html'
    success_url = 'evento/etiqueta/etiqueta_index.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = EtiquetaEvento
    form_class = EtiquetaEventoForm
    
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
        return redirect('/dashboard/evento/etiqueta/')


class EventoEtiquetaDelete(LoginRequiredMixin, DeleteView):
    template_name = 'evento/etiqueta/etiqueta_index.html'
    success_url = 'evento/etiqueta/etiqueta_index.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        etiquetaEvento = EtiquetaEvento.objects.get(id = self.kwargs['pk'])
        etiquetaEvento.delete()
        return redirect('/dashboard/evento/etiqueta/')


""" Aqui termina las vistas para el modulo de etiquetas de eventos """
