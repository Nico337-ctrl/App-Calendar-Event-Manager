from django.db.models.base import Model as Model
from django.shortcuts import render, redirect, get_object_or_404
from dashboard.models.usuarios import User
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import *
from django.urls import reverse_lazy
from django.db import IntegrityError
from dashboard.forms.users import *
from django.contrib.auth.decorators import login_required
from notifications.send_notification import enviarNotificacion
from notifications.emails.send_email import enviarEmail
from django.shortcuts import get_object_or_404, redirect

from datetime import timedelta
from django.utils import timezone

class SessionSignup(View):
    template_name= 'auth/signup.html'

    def get(self, request, *args, **kwargs):
        context = {'formulario' : User_CreationForm}
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
                    'formulario': User_CreationForm(),
                    'error': 'El nombre de usuario ya existe'
                }
                return render(request, self.template_name, context)
        else:
            context = {
                'formulario': User_CreationForm(),
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
        context = {'formulario':user_AuthenticationForm}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            context = { 'formulario' : user_AuthenticationForm, 'error' : 'Usuario o contraseña incorrectos'}
            return render(request, self.template_name, context)

        else:
            login(request, user)
            enviarNotificacion(titulo='App Calend Event Manager', mensaje='Su inicio de sesion ha sido exitoso')
            return redirect('home')

""" Aqui finaliza las vistas para el modulo de inicio de sesión"""
