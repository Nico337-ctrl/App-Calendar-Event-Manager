from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CustomEventForm, CustomAuthenticationForm, CustomUserCreationForm
from .models import evento_miembro
from django.contrib.auth.decorators import login_required
from notifications.send_notification import enviarNotificacion
# from notifications.emails.send_email import enviarEmail
from notifications.whatsapp.send_message import enviarMensajeWhats

# Create your views here.


#vista home o inicio
@login_required
def home_page(request):
    enviarNotificacion(titulo='App Calend Event Manager', mensaje='Bienvenido usuario')
    return render(request, 'home.html')

#vistas modulo usuario  
def session_signup(request):
    if request.method == 'GET':
        return render(request, 'auth/signup.html', {
            'formulario' : CustomUserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #registrando usuario
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                enviarNotificacion(titulo='App Calend Event Manager', mensaje='Su registro ha sido exitoso')
                return redirect('home')
            except IntegrityError:
                return render(request, 'auth/signup.html', {
                    'formulario' : CustomUserCreationForm,
                    'error' : 'El nombre de usuario ya existe'
                })
        return render(request, 'auth/signup.html', {
                    'formulario' : CustomUserCreationForm,
                    'error' : 'La contraseña no coincide'
                })
        


def session_logout(request):
    logout(request)
    return redirect('/dashboard/auth/signin/')

def session_signin(request):
    if request.method == 'GET':
        return render(request, 'auth/signin.html', {
            'formulario' : CustomAuthenticationForm,
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'auth/signin.html', {
                'formulario' : CustomAuthenticationForm,
                'error' : 'Usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            enviarNotificacion(titulo='App Calend Event Manager', mensaje='Su inicio de sesion ha sido exitoso')
            return redirect('home')

#aqui finaliza las vistas para usuarios


#vistas modulo productos

@login_required
def evento_index(request):
    eventos = evento_miembro.objects.all()
    return render(request, 'evento/evento_index.html', {
        'eventos': eventos,
    })

@login_required
def evento_create(request):
    if request.method == 'GET':
        return render(request, 'evento/evento_create.html',{
            'formulario' : CustomEventForm
        })
    else:
        try:
            formulario = CustomEventForm(request.POST)
            nuevo_evento = formulario.save(commit=False)
            nuevo_evento.user = request.user
            nuevo_evento.save()
            enviarNotificacion(titulo='App Calend Event Manager', mensaje='Se ha registrado un evento de manera exitosa')
            return redirect('/dashboard/evento/')
        except ValueError:
            return render(request, 'evento/evento_create.html',{
                'formulario' : CustomEventForm,
                'error' : 'Porfavor ingrese datos validos.'
            })
        
@login_required
def evento_detail(request, evento_id):
    evento = get_object_or_404(evento_miembro, pk=evento_id)
    return render(request, 'evento/evento_detail.html', {
        'evento': evento
    })

@login_required
def evento_edit(request, evento_id):
    if request.method == 'GET':
        evento = get_object_or_404(evento_miembro, pk=evento_id)
        formulario = CustomEventForm(instance=evento)
        return render(request, 'evento/evento_edit.html', {
            'formulario': formulario,
            'evento' : evento
        })
    else:
        try:
            evento = get_object_or_404(evento_miembro, pk=evento_id)
            formulario = CustomEventForm(request.POST, instance=evento)
            if formulario.is_valid():
                #validacion de formulario
                formulario.save()
                return redirect('/dashboard/evento/')
        except:
            return render(request, 'evento/evento_edit.html', {
            'formulario': formulario,
            'error' : 'algo no esta funcionando bien '
        })

@login_required
def evento_delete(request, evento_id):
        evento = evento_miembro.objects.get(id = evento_id)
        evento.delete()
        return redirect('/dashboard/evento/')

#aqui termina las vistas para el modulo productos


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