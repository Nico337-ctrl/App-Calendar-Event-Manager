from django.urls import path
from . import views

urlpatterns = [
    
    #rutas modulo usuario
    path('auth/signup/', views.session_signup, name='signup'),
    path('auth/logout/', views.session_logout, name='logout'),
    path('auth/signin/', views.session_signin, name='signin'),

    #ruta home o inicio
    path('home/', views.home_page, name='home'),

    #rutas modulo eventos
    path('eventos/create/', views.eventos_create, name='eventos_create'),
    path('eventos/', views.eventos_index, name='eventos'),    
    path('eventos/detail/<int:evento_miembro_id>', views.eventos_detail, name='eventos_detail'),
    path('eventos/edit/<int:evento_miembro_id>', views.eventos_edit, name='eventos_edit'),
    path('eventos/delete/<int:evento_miembro_id>', views.evento_delete, name='eventos_delete'),
    
    #rutas modulo usuarios
    path('usuario/create/', views.usuarios_create, name='usuario_create'),
    path('usuario/', views.usuarios_index, name='usuario'),    
    path('usuario/detail/<int:usuario_id>', views.usuarios_detail, name='usuario_detail'),
    path('usuario/edit/<int:usuario_id>', views.usuarios_edit, name='usuario_edit'),
    path('usuario/delete/<int:usuario_id>', views.usuarios_delete, name='usuario_delete'),
    
]