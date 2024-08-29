from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

# Cargar variables de entorno
load_dotenv()

def enviar_correo(destinatario, asunto, template_name, variables_html):
    """
    Envía un correo electrónico con contenido HTML dinámico.

    :param destinatario: Dirección de correo del destinatario.
    :param asunto: Asunto del correo.
    :param template_name: Nombre del archivo HTML de la plantilla (ej. 'email.html').
    :param variables_html: Diccionario con las variables a renderizar en la plantilla.
    """
    remitente = os.getenv('USER')
    
    # Cargar la plantilla HTML utilizando Jinja2
    env = Environment(loader=FileSystemLoader('C:/Workspace/App EventosCalendario/notifications/emails/'))
    template = env.get_template(template_name)
    html_renderizado = template.render(variables_html)

    # Preparar el mensaje con contenido HTML dinámico
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(html_renderizado, 'html'))

    # Configurar servidor SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, os.getenv('PASS'))

    # Enviar el correo
    server.sendmail(remitente, destinatario, msg.as_string())
    server.quit()

# Ejemplo de uso
# if __name__ == '__main__':
#     destinatario = 'ojedacorreanicolas@gmail.com'
#     asunto = 'Testeando Correo Dinámico'
#     template_name = 'email.html'
#     variables_html = {
#         'nombre_usuario': 'Nicolás Ojeda',
#         'evento': 'Reunión de Proyecto',
#         'fecha_evento': '2024-08-30',
#         'lugar_evento': 'Sala de Conferencias 1'
#     }

#     enviar_correo(destinatario, asunto, template_name, variables_html)
