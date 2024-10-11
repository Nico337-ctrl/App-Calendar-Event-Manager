from django.urls import include, path

urlpatterns = [
    path('auth/', include('dashboard.urls.auth.auth_urls')),
    path('', include('dashboard.urls.home.home_urls')),
    path('evento/', include('dashboard.urls.eventos.evento_urls')),
    path('evento/etiqueta/', include('dashboard.urls.eventos.eventoEtiqueta_urls')),
    path('registro/', include('dashboard.urls.registros.registro_urls')),
    path('calendario/', include('dashboard.urls.calendario.calendario_urls')),
    path('usuario/', include('dashboard.urls.usuarios.usuarios_urls')),

]