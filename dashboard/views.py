from django.db.models.base import Model as Model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from django.urls import reverse_lazy
from django.db import IntegrityError
from .forms import CustomEventForm, CustomAuthenticationForm, CustomUserCreationForm, CustomUserChangeForm
from .models import EventoMiembro
from django.contrib.auth.decorators import login_required
from notifications.send_notification import enviarNotificacion
from notifications.emails.send_email import enviarEmail
from dashboard.auto_notificacion import enviar_notificaciones
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

""" Aqui comienzan las vistas del modulo usuario """
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

""" Aqui finaliza las vistas para el modulo de usuario"""



""" Aqui comienzan las vistas para el modulo de eventos """

class EventoIndex(LoginRequiredMixin, ListView):
    template_name= 'evento/evento_index.html'
    queryset = EventoMiembro.objects.all()
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
    model = EventoMiembro
    context_object_name = 'evento'
        
        

class EventoEdit(LoginRequiredMixin, UpdateView):
    template_name = 'evento/evento_edit.html'
    success_url = 'evento/evento_index.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = EventoMiembro
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
    # template_name = 'evento/evento_edit.html'
    success_url = 'evento/evento_index.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        evento = EventoMiembro.objects.get(id = self.kwargs['pk'])
        evento.delete()
        return redirect('/dashboard/evento/')




# def calcular_intervalos(fecha_inicio, fecha_fin, num_intervalos=3):
#     duracion = fecha_fin - fecha_inicio
#     intervalos = []
#     for i in range(num_intervalos):
#         intervalo_inicio = fecha_inicio + i * (duracion / num_intervalos)
#         intervalo_fin = fecha_inicio + (i + 1) * (duracion / num_intervalos)
#         intervalos.append((intervalo_inicio, intervalo_fin))
#     return intervalos


# def ejecutar_acciones():
#     eventos = EventoMiembro.objects.all()
#     for evento in eventos:
#         intervalos = calcular_intervalos(evento.comienza, evento.termina)
#         for intervalo in intervalos:
#             realizar_accion(evento, intervalo[0], intervalo[1])

# def realizar_accion(evento, intervalo_inicio, intervalo_fin):
#     # Aquí defines la acción que deseas realizar
#     enviarNotificacion(titulo='App Calend Event Manager', mensaje='Recuerda que el evento')
#     enviarEmail(destinatario='ojedacorreanicolas@gmail.com', asunto='Haz sido invitado a este evento')
#     print(f"Realizando acción para {evento.titulo} del {intervalo_inicio.strftime('%d-%m-%Y %H:%M')} al {intervalo_fin.strftime('%d-%m-%Y %H:%M')}")

# # Ejecutar las acciones
# ejecutar_acciones()






""" Aqui termina las vistas para el modulo de eventos """


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
    template_name = 'usuario/usuaro_detail.html'
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
        evento = EventoMiembro.objects.get(id = self.kwargs['pk'])
        evento.delete()
        return redirect('/dashboard/usuario/')



""" Aqui terminan las vistas para el modulo usuarios """

""" Aqui comienzan las vistas para el template calendario """

def calendario_index(request):
    eventos = EventoMiembro.objects.all()
    return render(request, 'calendario/calendario.html', {
        'eventos' : eventos,
    })

""" Aqui terminan las vistas para el template calendario """