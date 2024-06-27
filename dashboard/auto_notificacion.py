from datetime import timedelta
from django.utils import timezone
from .models import evento_miembro
from notifications.send_notification import enviarNotificacion
from notifications.emails.send_email import enviarEmail

def realizar_accion(evento, momento):
    # Aquí defines la acción que deseas realizar
    if momento == '20 minutos antes':
        enviarNotificacion(titulo='App Calend Event Manager', mensaje=f'Recuerda que el evento {evento.titulo} comienza en 20 minutos.')
    elif momento == 'inicio del evento':
        enviarNotificacion(titulo='App Calend Event Manager', mensaje=f'El evento {evento.titulo} ha comenzado.')
        enviarEmail(destinatario='ojedacorreanicolas@gmail.com', asunto=f'El evento {evento.titulo} ha comenzado.')
    elif momento == 'fin del evento':
        enviarNotificacion(titulo='App Calend Event Manager', mensaje=f'El evento {evento.titulo} ha terminado.')
    print(f"Realizando acción para {evento.titulo} en el momento: {momento}")

def enviar_notificaciones():
    ahora = timezone.now()
    eventos = evento_miembro.objects.filter(comienza__lte=ahora + timedelta(minutes=20), termina__gte=ahora)
    
    for evento in eventos:
        if ahora >= evento.comienza - timedelta(minutes=20):
            realizar_accion(evento, '20 minutos antes')
        if ahora >= evento.comienza:
            realizar_accion(evento, 'inicio del evento')
        if ahora >= evento.termina:
            realizar_accion(evento, 'fin del evento')

