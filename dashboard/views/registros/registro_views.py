from django.db.models.base import Model as Model
# from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import *
# from dashboard.forms.eventos.eventos_forms import FormEventos
from dashboard.models.registros import Registros
from dashboard.views.mixins import *
# from notifications.send_notification import enviarNotificacion
# from django.contrib import messages

class RegistroIndex(LoginRequiredMixin, PermissionRequiredMixin,  UserGroupContextMixin ,ListView):
    template_name= 'registro/registro_index.html'
    queryset = Registros.objects.all()
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'registros'
    permission_required = 'dashboard.view_user'
    

