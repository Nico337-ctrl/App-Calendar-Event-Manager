from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from dashboard.models.usuarios import User
from django.contrib.auth.models import Group


class User_CreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2' , 'first_name', 'last_name', 'email', 'telefono', 'imagen', 'group']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].label_from_instace = lambda obj: obj.name
    
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
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(
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