from django.urls import path
from dashboard.views import *

urlpatterns = [
    path('create/', UsuarioCreate.as_view(), name='usuario_create'),
    path('', UsuarioIndex.as_view(), name='usuario'),
    path('detail/<int:pk>', UsuarioDetail.as_view(), name='usuario_detail'),
    path('edit/<int:pk>', UsuarioEdit.as_view(), name='usuario_edit'),
    path('delete/<int:pk>', UsuarioDelete.as_view(), name='usuario_delete'),
    path('changePassword/<int:pk>', UsuarioChangePassword.as_view(), name='usuario_changePassword'),
    path('profile/<int:pk>', UsuarioProfile.as_view(), name='usuario_profile'),

]
