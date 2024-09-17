from django.urls import path
from dashboard.views import *

urlpatterns = [
    path('', RegistroIndex.as_view(), name='registro'), 
    path('detail/<int:pk>', RegistroDetail.as_view(), name='registro_detail'),
]