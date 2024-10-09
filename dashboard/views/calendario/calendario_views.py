from django.db.models.base import Model as Model
# from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
# from dashboard.forms.eventos.eventos_forms import FormEventos
from dashboard.models import Eventos
# from notifications.send_notification import enviarNotificacion
# from django.contrib import messages
from dashboard.views.mixins import *



class CalendarioIndex(LoginRequiredMixin, UserGroupContextMixin, ListView):
    template_name= 'calendario/calendario.html'
    queryset = Eventos.objects.all()
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'eventos'

