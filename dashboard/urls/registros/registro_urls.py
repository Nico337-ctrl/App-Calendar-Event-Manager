from django.urls import path
from dashboard.views import *

urlpatterns = [
    path('', RegistroIndex.as_view(), name='registro'), 
]