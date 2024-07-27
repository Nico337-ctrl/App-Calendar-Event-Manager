from django.urls import path
from dashboard.views import *

urlpatterns = [
path('create/', EventoCreate.as_view(), name='evento_create'),
path('', EventoIndex.as_view(), name='evento'),
path('detail/<int:pk>', EventoDetail.as_view(), name='evento_detail'),
path('edit/<int:pk>', EventoEdit.as_view(), name='evento_edit'),
path('delete/<int:pk>', EventoDelete.as_view(), name='evento_delete'),
]