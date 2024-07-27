from django.urls import path
from dashboard.views import *


urlpatterns = [
path('create/', EventoEtiquetaCreate.as_view(), name='evento_etiqueta_create'),
path('', EventoEtiquetaIndex.as_view(), name='evento_etiqueta'),
path('detail/<int:pk>', EventoEtiquetaDetail.as_view(), name='evento_etiqueta_detail'),
path('edit/<int:pk>', EventoEtiquetaEdit.as_view(), name='evento_etiqueta_edit'),
path('delete/<int:pk>', EventoEtiquetaDelete.as_view(), name='evento_etiqueta_delete')
]