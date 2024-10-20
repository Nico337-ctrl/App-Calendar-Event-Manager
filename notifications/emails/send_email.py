from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader


load_dotenv()

def enviar_correo(destinatarios, asunto, datos):
    """
    Envía un correo electrónico con contenido HTML dinámico.

    :param destinatarios: Lista de direcciones de correo de los destinatarios.
    :param asunto: Asunto del correo.
    :param variables_html: Diccionario con las variables a renderizar en la plantilla.
    """
    remitente = os.getenv('USER')

    # Obtener el directorio del script actual y construir la ruta de la plantilla HTML
    script_dir = os.path.dirname(os.path.realpath(__file__))
    ruta_plantilla = os.path.join(script_dir, 'email.html')

    # Cargar la plantilla HTML utilizando Jinja2
    env = Environment(loader=FileSystemLoader(os.path.dirname(ruta_plantilla)))
    template = env.get_template(os.path.basename(ruta_plantilla))
    html_renderizado = template.render(datos)

    for destinatario in destinatarios:
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
        print(f'Se envió un correo a {destinatario}')
        server.quit()

