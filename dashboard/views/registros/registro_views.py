from django.db.models.base import Model as Model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import *
from dashboard.models.registros import Registros
from dashboard.views.mixins import *

class RegistroIndex(LoginRequiredMixin, ValidarPermisosRequeridosMixin,  UserGroupContextMixin ,ListView):
    template_name= 'registro/registro_index.html'
    queryset = Registros.objects.all()
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'registros'
    permission_required = 'dashboard.view_user'


class RegistroDetail(LoginRequiredMixin, ValidarPermisosRequeridosMixin,DetailView):
    template_name = 'registro/registro_detail.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    model = Registros
    context_object_name = 'registro'
    permission_required = 'dashboard.view_user'



    

