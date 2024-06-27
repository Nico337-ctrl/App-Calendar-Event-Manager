from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv()
# Configuración de Mailtrap
# remitente = os.getenv('USER')
# destinatario = 'ojedacorreanicolas@gmail.com'
# asunto = 'testeando'

# msg = MIMEMultipart()

# email = EmailMessage()
# email['From'] = remitente
# email['To'] = destinatario
# email['Subject'] = 'email test'

# with open('C:/Workspace/App EventosCalendario/notifications/emails/email.html', 'r') as archivo:
#     html = archivo.read()

# msg.attach(MIMEText(html, 'html'))

# server = smtplib.SMTP('smtp.gmail.com', 587)

# server.starttls()
# server.login(remitente, os.getenv('PASS'))

# server.sendmail(remitente, destinatario, msg.as_string())
# server.quit()


def enviarEmail(destinatario, asunto):
    remitente = os.getenv('USER')
    msg = MIMEMultipart()
    email = EmailMessage()
    email['From'] = remitente
    email['To'] = destinatario
    email['Subject'] = asunto

    with open('C:/Workspace/App EventosCalendario/notifications/emails/email.html', 'r') as archivo:
        html = archivo.read()

    msg.attach(MIMEText(html, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()
    server.login(remitente, os.getenv('PASS'))

    server.sendmail(remitente, destinatario, msg.as_string())
    server.quit()

    
    