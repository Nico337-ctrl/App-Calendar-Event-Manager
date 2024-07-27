from django.urls import path
from dashboard.views import *


urlpatterns = [
path('home/', HomeDashboard.as_view(), name='home'),
]