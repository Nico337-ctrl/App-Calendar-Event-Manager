from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'


    def ready(self):
        import dashboard.signals.eventos.eventos_signals
        import dashboard.signals.eventos.etiquetas_signals
        import dashboard.signals.eventos.notificarEvento_signals
        import dashboard.signals.registros.tipoRegistro_signals
        import dashboard.signals.registros.entidadRegistro_signals 
        import dashboard.signals.usuarios.usuario_correo_signals
        import dashboard.signals.usuarios.usuarios_signals
        import dashboard.signals.usuarios.roles_signals