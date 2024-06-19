from django.forms import ModelForm
from .models import evento_miembro
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class event_form(ModelForm):
    class Meta:
        model = evento_miembro
        fields = ['usuario', 'titulo', 'descripcion', 'comienza', 'termina']
        
class CustomEventForm(forms.ModelForm):
    class Meta:
        model = evento_miembro
        fields = ['usuario', 'titulo', 'descripcion', 'comienza', 'termina']
    
    usuario = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
                'placeholder': 'Usuario',
                'aria-label': 'Usuario',
                'aria-describedby': 'usuario-addon'
            }
        )
    )
    titulo = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
                'placeholder': 'Titulo',
                'aria-label': 'Titulo',
                'aria-describedby': 'Titulo-addon'
            }
        )
    )
    descripcion = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
                'placeholder': 'desdescripcion',
                'aria-label': 'descripcion',
                'aria-describedby': 'descripcion-addon'
            }
        )
    )
    comienza = forms.CharField(
        widget=forms.DateTimeInput(
            attrs={
                'class': '',
                'placeholder': '',
                'aria-label': '',
                'aria-describedby': ''
            }
        )
    )
    termina = forms.CharField(
        widget=forms.DateTimeInput(
            attrs={
                'class': '',
                'placeholder': '',
                'aria-label': '',
                'aria-describedby': ''
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
    