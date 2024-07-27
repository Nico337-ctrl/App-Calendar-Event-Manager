from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *


class HomeDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'

