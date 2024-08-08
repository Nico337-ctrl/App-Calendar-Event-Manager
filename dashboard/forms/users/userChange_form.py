from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from django import forms
from dashboard.models.usuarios import User

class User_ChangeForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'imagen']
    
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                    
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                    
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                    
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                    
            }
        )
    )
    telefono = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                    
            }
        )
    )
    imagen = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                    'class': 'form-control',
                }
            ),
        required=False
        )