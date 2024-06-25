from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db import IntegrityError
from .forms import CustomEventForm, CustomAuthenticationForm, CustomUserCreationForm
from .models import evento_miembro
from django.contrib.auth.decorators import login_required
from notifications.send_notification import enviarNotificacion
# from notifications.emails.send_email import enviarEmail
from notifications.whatsapp.send_message import enviarMensajeWhats

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
    queryset = evento_miembro.objects.all()
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'eventos'



class EventoCreate(LoginRequiredMixin, CreateView):
    template_name = 'evento/evento_create.html'
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
            enviarNotificacion(titulo='App Calend Event Manager', mensaje='Se ha registrado un evento de manera exitosa')
            return redirect('/dashboard/evento/')
        except ValueError:
            context = {'formulario' : CustomEventForm, 'error' : 'Porfavor ingrese datos validos.'}
            return render(request, self.template_name, context)
            
            
class EventoDetail(LoginRequiredMixin, DetailView):
    template_name = 'evento/evento_detail.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = evento_miembro
    context_object_name = 'evento'
        
        
class EventoEdit(LoginRequiredMixin, UpdateView):
    template_name = 'evento/evento_edit.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = evento_miembro
    form_class = CustomEventForm
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(evento_miembro, pk=pk)

    def form_valid(self, form):
        instacia = form.save(commit=False)
        instacia.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, error='Los datos ingresados no son del todo correctos.'))

    def get_success_url(self):
        return reverse_lazy('evento/evento_index.html')

# @login_required
# def evento_edit(request, evento_id):
#     if request.method == 'GET':
#         evento = get_object_or_404(evento_miembro, pk=evento_id)
#         formulario = CustomEventForm(instance=evento)
#         return render(request, 'evento/evento_edit.html', {
#             'formulario': formulario,
#             'evento' : evento
#         })
#     else:
#         try:
#             evento = get_object_or_404(evento_miembro, pk=evento_id)
#             formulario = CustomEventForm(request.POST, instance=evento)
#             if formulario.is_valid():
#                 #validacion de formulario
#                 formulario.save()
#                 return redirect('/dashboard/evento/')
#         except:
#             return render(request, 'evento/evento_edit.html', {
#             'formulario': formulario,
#             'error' : 'algo no esta funcionando bien '
#         })

@login_required
def evento_delete(request, evento_id):
        evento = evento_miembro.objects.get(id = evento_id)
        evento.delete()
        return redirect('/dashboard/evento/')

""" Aqui termina las vistas para el modulo de eventos """


#aqui comienza las vistas para el modulo usuarios
@login_required
def usuarios_index(request):
    usuarios = User.objects.all()
    return render(request, 'usuario/usuario_index.html', {
        'usuarios' : usuarios
    })


@login_required
def usuarios_create(request):
    if request.method == 'GET':
        return render(request, 'usuario/usuario_create.html',{
            'formulario' : CustomUserCreationForm
        
        })

    else:
        try:
            formulario = CustomUserCreationForm(request.POST)
            if formulario.is_valid():
                nuevo_usuario = formulario.save()
                nuevo_usuario.save()
                return redirect('usuario')
        except ValueError:
            return render(request, 'usuario/usuario_create.html',{
                'formulario' : CustomUserCreationForm,
                'error' : 'Porfavor ingrese datos validos'
            })

@login_required
def usuarios_detail(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    return render(request, 'usuario/usuario_detail.html', {
        'usuario': usuario
    })

@login_required
def usuarios_edit(request, usuario_id):
    if request.method == 'GET':
        usuario = get_object_or_404(User, pk=usuario_id)
        formulario = CustomUserCreationForm(instance=usuario)
        return render(request, 'usuario/usuario_edit.html', {
            'formulario': formulario,
            'usuario' : usuario
        })
    else:
        try:
            usuario = get_object_or_404(User, pk=usuario_id)
            formulario = CustomUserCreationForm(request.POST, instance=usuario_id)
            if formulario.is_valid():
                #validacion de formulario
                formulario.save()
                return redirect('usuario')
        except:
            return render(request, 'usuario/usuario_edit.html', {
            'formulario': formulario,
            'error' : 'algo no esta funcionando bien'
        })

@login_required
def usuarios_delete(request, usuario_id):
        usuario = User.objects.get(id = usuario_id)
        usuario.delete()
        return redirect('/dashboard/usuario/')

# Aqui comienza la vista del calendario

def calendario_index(request):
    eventos = evento_miembro.objects.all()
    return render(request, 'calendario/calendario.html', {
        'eventos' : eventos,
    })