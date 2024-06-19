from django.urls import path
from . import views

urlpatterns = [
    
    #rutas modulo usuario
    path('auth/signup/', views.session_signup, name='signup'),
    path('auth/logout/', views.session_logout, name='logout'),
    path('auth/signin/', views.session_signin, name='signin'),

    #ruta home o inicio
    path('home/', views.home_page, name='home'),

    #rutas modulo productos
    path('producto/create/', views.productos_create, name='producto_create'),
    path('producto/', views.productos_index, name='producto'),    
    path('producto/detail/<int:producto_id>', views.productos_detail, name='producto_detail'),
    path('producto/edit/<int:producto_id>', views.productos_edit, name='producto_edit'),
    
    #rutas modulo usuarios
    path('usuario/create/', views.usuarios_create, name='usuario_create'),
    path('usuario/', views.usuarios_index, name='usuario'),    
    path('usuario/detail/<int:usuario_id>', views.usuarios_detail, name='usuario_detail'),
    path('usuario/edit/<int:usuario_id>', views.usuarios_edit, name='usuario_edit'),
    
]