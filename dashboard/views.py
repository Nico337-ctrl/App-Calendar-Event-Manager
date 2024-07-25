from django.db.models.base import Model as Model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import *
from django.urls import reverse_lazy
from django.db import IntegrityError
from .forms import CustomEventForm,  CustomEtiqEventForm, CustomAuthenticationForm, CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm
from .models import Eventos, EtiquetaEvento, Registros
from django.contrib.auth.decorators import login_required
from notifications.send_notification import enviarNotificacion
from notifications.emails.send_email import enviarEmail
from dashboard.auto_notificacion import enviar_notificaciones
from django.shortcuts import get_object_or_404, redirect
# from notifications.whatsapp.send_message import enviarMensajeWhats
from datetime import timedelta
from django.utils import timezone

# Create your views here.


""" Aqui comienzan las vistas Home de la dashboard """
class HomeDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'

""" Aqui terminan las vistas Home de la dashboard """

""" Aqui comienzan las vistas del modulo de inicio de sesión """
class SessionSignup(View):
    template_name= 'auth/signup.html'

    def get(self, request, *args, **kwargs):
        context = {'formulario' : CustomUserCreationForm}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Registrando usuario
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                enviarNotificacion(titulo='App Calend Event Manager', mensaje='Su registro ha sido exitoso')
                # enviarMensajeWhats('+573223829018', 'Hola, te habla tu plataforma de Eventos SENA, tu registro ha sido exitoso.')
                return redirect('home')
            except IntegrityError:
                context = {
                    'formulario': CustomUserCreationForm(),
                    'error': 'El nombre de usuario ya existe'
                }
                return render(request, self.template_name, context)
        else:
            context = {
                'formulario': CustomUserCreationForm(),
                'error': 'La contraseña no coincide'
            }
            return render(request, self.template_name, context)
        
            
class SessionLogout(TemplateView):
    template_name = 'signin'
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy(self.template_name))


class SessionSignin(View):
    template_name = 'auth/signin.html'
    
    def get(self, request, *args, **kwargs):
        context = {'formulario':CustomAuthenticationForm}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            context = { 'formulario' : CustomAuthenticationForm, 'error' : 'Usuario o contraseña incorrectos'}
            return render(request, self.template_name, context)

        else:
            login(request, user)
            enviarNotificacion(titulo='App Calend Event Manager', mensaje='Su inicio de sesion ha sido exitoso')
            return redirect('home')

""" Aqui finaliza las vistas para el modulo de inicio de sesión"""


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
        context = {'formulario' : CustomEventForm}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            formulario = CustomEventForm(request.POST)
            nuevo_evento = formulario.save(commit=False)
            nuevo_evento.user = request.user
            nuevo_evento.etiqueta = request
            nuevo_evento.save()
            enviar_notificaciones()
            return redirect(self.success_url)
        except ValueError:
            context = {'formulario' : CustomEventForm, 'error' : 'Porfavor ingrese datos validos.'}
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
    form_class = CustomEventForm
    
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
        context = {'formulario' : CustomEtiqEventForm}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            formulario = CustomEtiqEventForm(request.POST)
            nueva_etiqueta = formulario.save(commit=False)
            nueva_etiqueta.save()
            enviar_notificaciones()
            return redirect(self.success_url)
        except ValueError:
            context = {'formulario' : CustomEtiqEventForm, 'error' : 'Porfavor ingrese datos validos.'}
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
    form_class = CustomEtiqEventForm
    
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
        etiquetaEvento = Eventos.objects.get(id = self.kwargs['pk'])
        etiquetaEvento.delete()
        return redirect('/dashboard/evento/etiqueta/')


""" Aqui termina las vistas para el modulo de etiquetas de eventos """


""" Aqui comienzan las vistas para el modulo de usuarios"""

class UsuarioIndex(LoginRequiredMixin, ListView):
    template_name= 'usuario/usuario_index.html'
    queryset = User.objects.all()
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'usuarios'


class UsuarioCreate(LoginRequiredMixin, CreateView):
    template_name = 'usuario/usuario_create.html'
    success_url = '/dashboard/usuario/'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        context = {'formulario' : CustomEventForm}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            formulario = CustomUserCreationForm(request.POST)
            nuevo_usuario = formulario.save(commit=False)
            nuevo_usuario.save()
            enviar_notificaciones()
            return redirect(self.success_url)
        except ValueError:
            context = {'formulario' : CustomUserCreationForm, 'error' : 'Porfavor ingrese datos validos.'}
            return render(request, self.template_name, context)
        


class UsuarioDetail(LoginRequiredMixin, DetailView):
    template_name = 'usuario/usuario_detail.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = User
    context_object_name = 'usuario'




class UsuarioEdit(LoginRequiredMixin, UpdateView):
    template_name = 'usuario/usuario_edit.html'
    success_url = 'usuario/usuario_index.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = User
    form_class = CustomUserChangeForm
    
    def get(self, request, *args, **kwargs):
        usuario = get_object_or_404(self.model, pk=self.kwargs['pk'])
        formulario = self.form_class(instance=usuario)
        context = {'usuario': usuario, 'formulario': formulario}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        usuario = get_object_or_404(self.model, pk=self.kwargs['pk'])
        formulario = self.form_class(request.POST, instance=usuario)
        if formulario.is_valid():
            formulario.save()
        return redirect('/dashboard/usuario/')
    


class UsuarioDelete(LoginRequiredMixin, DeleteView):
    # template_name = 'usuario/evento_edit.html'
    success_url = 'usuario/usuario_index.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        usuario = User.objects.get(id = self.kwargs['pk'])
        usuario.delete()
        return redirect('/dashboard/usuario/')


class UsuarioChangePassword(LoginRequiredMixin, View):
    model = User
    template_name = 'usuario/usuario_changePassword.html'
    success_url = '/dashboard/usuario/'

    def get(self, request, *args, **kwargs):
        usuario = get_object_or_404(self.model, pk=self.kwargs['pk'])
        formulario = CustomPasswordChangeForm(user=request.user)
        context = {'usuario': usuario, 'formulario': formulario}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        usuario = get_object_or_404(self.model, pk=self.kwargs['pk'])
        formulario = CustomPasswordChangeForm(user=request.user, data=request.POST)
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
    


""" Aqui terminan las vistas para el modulo usuarios """

""" Aqui comienzan las vistas para el template calendario """

class CalendarioIndex(LoginRequiredMixin, ListView):
    template_name= 'calendario/calendario.html'
    queryset = Eventos.objects.all()
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'eventos'

""" Aqui terminan las vistas para el template calendario """


""" Aqui comienzan las vistas para el modulo de registros """
class RegistroIndex(LoginRequiredMixin, ListView):
    template_name= 'registro/registro_index.html'
    queryset = Registros.objects.all()
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'registros'

""" Aqui terminan las vistas para el modulo de registros """

