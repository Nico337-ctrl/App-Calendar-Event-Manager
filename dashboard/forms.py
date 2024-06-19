from django.forms import ModelForm
from .models import Productos
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class producto_form(ModelForm):
    class Meta:
        model = Productos
        fields = ['codigo', 'descripcion', 'precio', 'cantidad']
        
class CustomProductoForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['codigo', 'descripcion', 'precio', 'cantidad']
    
    codigo = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'focus:shadow-soft-primary-outline text-sm leading-5.6 ease-soft block w-full appearance-none rounded-lg border border-solid border-gray-300 bg-white bg-clip-padding px-3 py-2 font-normal text-gray-700 transition-all focus:border-fuchsia-300 focus:outline-none focus:transition-shadow',
                'placeholder': 'Código',
                'aria-label': 'Código',
                'aria-describedby': 'codigo-addon'
            }
        )
    )
    descripcion = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'focus:shadow-soft-primary-outline text-sm leading-5.6 ease-soft block w-full appearance-none rounded-lg border border-solid border-gray-300 bg-white bg-clip-padding px-3 py-2 font-normal text-gray-700 transition-all focus:border-fuchsia-300 focus:outline-none focus:transition-shadow',
                'placeholder': 'Descripción',
                'aria-label': 'Descripción',
                'aria-describedby': 'descripcion-addon'
            }
        )
    )
    precio = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'focus:shadow-soft-primary-outline text-sm leading-5.6 ease-soft block w-full appearance-none rounded-lg border border-solid border-gray-300 bg-white bg-clip-padding px-3 py-2 font-normal text-gray-700 transition-all focus:border-fuchsia-300 focus:outline-none focus:transition-shadow',
                'placeholder': 'Precio',
                'aria-label': 'Precio',
                'aria-describedby': 'precio-addon'
            }
        )
    )
    cantidad = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'focus:shadow-soft-primary-outline text-sm leading-5.6 ease-soft block w-full appearance-none rounded-lg border border-solid border-gray-300 bg-white bg-clip-padding px-3 py-2 font-normal text-gray-700 transition-all focus:border-fuchsia-300 focus:outline-none focus:transition-shadow',
                'placeholder': 'Cantidad',
                'aria-label': 'Cantidad',
                'aria-describedby': 'cantidad-addon'
            }
        )
    )


# class CustomProductoForm(producto_form):
    







class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'focus:shadow-soft-primary-outline text-sm leading-5.6 ease-soft block w-full appearance-none rounded-lg border border-solid border-gray-300 bg-white bg-clip-padding px-3 py-2 font-normal text-gray-700 transition-all focus:border-fuchsia-300 focus:outline-none focus:transition-shadow',
                'placeholder': 'Username',
                'aria-label': 'Username',
                'aria-describedby': 'user-addon'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'focus:shadow-soft-primary-outline text-sm leading-5.6 ease-soft block w-full appearance-none rounded-lg border border-solid border-gray-300 bg-white bg-clip-padding px-3 py-2 font-normal text-gray-700 transition-all focus:border-fuchsia-300 focus:outline-none focus:transition-shadow',
                'placeholder': 'Password',
                'aria-label': 'Password',
                'aria-describedby': 'password-addon'
            }
        )
    )


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'focus:shadow-soft-primary-outline text-sm leading-5.6 ease-soft block w-full appearance-none rounded-lg border border-solid border-gray-300 bg-white bg-clip-padding px-3 py-2 font-normal text-gray-700 transition-all focus:border-fuchsia-300 focus:outline-none focus:transition-shadow',
                'placeholder': 'Username',
                'aria-label': 'Username',
                'aria-describedby': 'user-addon'
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'focus:shadow-soft-primary-outline text-sm leading-5.6 ease-soft block w-full appearance-none rounded-lg border border-solid border-gray-300 bg-white bg-clip-padding px-3 py-2 font-normal text-gray-700 transition-all focus:border-fuchsia-300 focus:outline-none focus:transition-shadow',
                'placeholder': 'Password',
                'aria-label': 'Password',
                'aria-describedby': 'password-addon'
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'focus:shadow-soft-primary-outline text-sm leading-5.6 ease-soft block w-full appearance-none rounded-lg border border-solid border-gray-300 bg-white bg-clip-padding px-3 py-2 font-normal text-gray-700 transition-all focus:border-fuchsia-300 focus:outline-none focus:transition-shadow',
                'placeholder': 'Password',
                'aria-label': 'Password',
                'aria-describedby': 'password-addon'
            }
        )
    )
    