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
    path('evento/create/', views.evento_create, name='evento_create'),
    path('evento/', views.evento_index, name='evento'),    
    path('evento/detail/<int:evento_id>', views.evento_detail, name='evento_detail'),
    path('evento/edit/<int:evento_id>', views.evento_edit, name='evento_edit'),
    path('evento/delete/<int:evento_id>', views.evento_delete, name='evento_delete'),
    
    #rutas modulo usuarios
    path('usuario/create/', views.usuarios_create, name='usuario_create'),
    path('usuario/', views.usuarios_index, name='usuario'),    
    path('usuario/detail/<int:usuario_id>', views.usuarios_detail, name='usuario_detail'),
    path('usuario/edit/<int:usuario_id>', views.usuarios_edit, name='usuario_edit'),
    path('usuario/delete/<int:usuario_id>', views.usuarios_delete, name='usuario_delete'),
    
    #rutas calendario
    path('calendario/', views.calendario_index, name='calendario'),
    
]