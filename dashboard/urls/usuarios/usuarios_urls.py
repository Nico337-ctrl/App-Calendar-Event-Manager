from django.urls import path
from dashboard.views import *
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('create/', UsuarioCreate.as_view(), name='usuario_create'),
    path('', UsuarioIndex.as_view(), name='usuario'),
    path('detail/<int:pk>', UsuarioDetail.as_view(), name='usuario_detail'),
    path('edit/<int:pk>', UsuarioEdit.as_view(), name='usuario_edit'),
    path('delete/<int:pk>', UsuarioDelete.as_view(), name='usuario_delete'),
    path('changePassword/<int:pk>', UsuarioChangePassword.as_view(), name='usuario_changePassword'),
    path('profile/<int:pk>', UsuarioProfile.as_view(), name='usuario_profile'),
    path('profile/upload/<int:pk>', UsuarioProfileEdit.as_view(), name='profile_upload'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
