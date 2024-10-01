from django.dispatch import receiver
from django.db.models.signals import *
from dashboard.models.eventos import Eventos
from dashboard.models.usuarios import User_Emails
from notifications.emails.send_email import enviar_correo

@receiver(post_save, sender=Eventos)
def creacion_evento(sender, instance, created, **kwargs):
    if created:
        titulo = instance.titulo
        descripcion = instance.descripcion 
        info_extra = instance.info_extra
        inicia_el = instance.inicia_el
        termina_el = instance.termina_el
        est_activo = instance.est_activo
        etiqueta = instance.descripcion

        evento = {
            'titulo': titulo,
            'descripcion': descripcion,
            'info_extra': info_extra,
            'inicia_el': inicia_el,
            'termina_el': termina_el,
            'est_activo': est_activo,
            'etiqueta': etiqueta
        }

        correos = User_Emails.objects.values_list('correo', flat=True)
        for correo in correos:
            enviar_correo(
                destinatario=correo,
                asunto=f'Se te invita a el evento: {titulo}',
                template_name='email_default.html', 
                variables_html=evento
            )   


        """Otra forma de realizar los envios"""
        # subject= f"Invitacion al evento {titulo}"
        # from_email = 'senaeventos782@gmail.com'
        # html_content = render_to_string('email_default.html', {
        #     'titulo_evento': titulo,
        #     'descripcion_evento': descripcion,
        #     'info_extra': info_extra,
        #     'inicia_el': inicia_el,
        #     'termina_el': termina_el,
        #     'etiqueta': etiqueta,
        #     'contacto': 'De SenaEventos.api'
        # })
        # text_content = strip_tags(html_content)
        # for correo in correos:
        #     to = [correo.email]  
        #     email = EmailMultiAlternatives(subject, text_content, from_email, to)
        #     email.attach_alternative(html_content, "text/html")
        #     email.send()


    