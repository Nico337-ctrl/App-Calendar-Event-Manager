from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'


    def ready(self):
        #signals registros
        import dashboard.signals.registros.tipo_registro_signals
        import dashboard.signals.registros.entidad_registro_signals 

        #signals registros-eventos, etiquetas
        import dashboard.signals.registros.eventos.registro_etiquetas_signals
        import dashboard.signals.registros.eventos.registro_eventos_signals

        #signals registros-usuarios, perfil
        import dashboard.signals.registros.usuarios.registro_usuarios_singals

        #signals usuarios
        import dashboard.signals.usuarios.roles_signals
        
        #signals perfil
        import dashboard.signals.usuarios.usuario_perfil_signals