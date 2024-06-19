from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CustomProductoForm, CustomAuthenticationForm, CustomUserCreationForm
from .models import Productos
from django.contrib.auth.decorators import login_required
# Create your views here.


#vista home o inicio

def home_page(request):
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
    return redirect('home')

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
            return redirect('home')

#aqui finaliza las vistas para usuarios


#vistas modulo productos

@login_required
def productos_index(request):
    productos = Productos.objects.all()
    return render(request, 'producto/producto_index.html', {
        'productos': productos,
    })

@login_required
def productos_create(request):
    if request.method == 'GET':
        return render(request, 'producto/producto_create.html',{
            'formulario' : CustomProductoForm
        })

    else:
        try:
            formulario = CustomProductoForm(request.POST)
            nuevo_producto = formulario.save(commit=False)
            nuevo_producto.user = request.user
            nuevo_producto.save()
            return redirect('producto')
        except ValueError:
            return render(request, 'producto/producto_create.html',{
                'formulario' : CustomProductoForm,
                'error' : 'Porfavor ingrese datos validos'
            })
@login_required
def productos_detail(request, producto_id):
    producto = get_object_or_404(Productos, pk=producto_id)
    return render(request, 'producto/producto_detail.html', {
        'producto': producto
    })

@login_required
def productos_edit(request, producto_id):
    if request.method == 'GET':
        producto = get_object_or_404(Productos, pk=producto_id)
        formulario = CustomProductoForm(instance=producto)
        return render(request, 'producto/producto_edit.html', {
            'formulario': formulario,
            'producto' : producto
        })
    else:
        try:
            producto = get_object_or_404(Productos, pk=producto_id)
            formulario = CustomProductoForm(request.POST, instance=producto)
            if formulario.is_valid():
                #validacion de formulario
                formulario.save()
                return redirect('producto')
        except:
            return render(request, 'producto/producto_edit.html', {
            'formulario': formulario,
            'error' : 'algo no esta funcionando bien '
        })

# @login_required
# def producto_delete(request, producto_id):
#     if request.method == 'GET':
#         producto = producto.id 

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
            usuario = get_object_or_404(Productos, pk=usuario_id)
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