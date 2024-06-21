from django.forms import ModelForm
from .models import evento_miembro
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class event_form(ModelForm):
    class Meta:
        model = evento_miembro
        fields = ['titulo', 'descripcion', 'comienza', 'termina']
        
class CustomEventForm(forms.ModelForm):
    class Meta:
        model = evento_miembro
        fields = ['titulo', 'descripcion', 'comienza', 'termina']
    
    # usuario = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #         }
    #     )
    # )
    titulo = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    descripcion = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    comienza = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'type' : 'datetime-local'
            }
        )
    )
    termina = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'type' : 'datetime-local'
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
                
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                
            }
        )
    )
    