from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from dashboard.views.mixins import *


class HomeDashboard(LoginRequiredMixin, UserGroupContextMixin ,TemplateView):
    template_name = 'home.html'
    login_url = '/dashboard/auth/signin/'
    redirect_field_name = 'redirect_to'
    
    

