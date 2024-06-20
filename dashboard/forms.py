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
                'class': 'form-control',
                'placeholder': 'Username',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }
        )
    )


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }
        )
    )
    