from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from dashboard.models.usuarios import User


class User_CreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2' , 'first_name', 'last_name', 'email']
    
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
    imagen = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                    'class': 'form-control',
                }
            ),
        required=False
        )
    
    
    
    # def save(self, commit=True):
    #     user = super(User_CreationForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data['password'])
    #     if commit:
    #         user.save()
    #     return user