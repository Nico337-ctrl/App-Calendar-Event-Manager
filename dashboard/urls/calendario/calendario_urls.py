from django.urls import path
from dashboard.views import *


urlpatterns = [
path('', CalendarioIndex.as_view(), name='calendario'),
]