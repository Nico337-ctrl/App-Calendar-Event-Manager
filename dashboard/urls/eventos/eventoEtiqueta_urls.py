from django.urls import path
from dashboard.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
path('create/', EventoEtiquetaCreate.as_view(), name='evento_etiqueta_create'),
path('', EventoEtiquetaIndex.as_view(), name='evento_etiqueta'),
path('detail/<int:pk>', EventoEtiquetaDetail.as_view(), name='evento_etiqueta_detail'),
path('edit/<int:pk>', EventoEtiquetaEdit.as_view(), name='evento_etiqueta_edit'),
path('delete/<int:pk>', EventoEtiquetaDelete.as_view(), name='evento_etiqueta_delete')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)