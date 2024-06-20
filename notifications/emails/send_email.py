from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv()
# Configuración de Mailtrap
remitente = os.getenv('USER')
destinatario = 'samirdelportillo01@gmail.com'
asunto = 'testeando'

msg = MIMEMultipart()

email = EmailMessage()
email['From'] = remitente
email['To'] = destinatario
email['Subject'] = 'email test'

with open('notifications/emails/email.html', 'r') as archivo:
    html = archivo.read()

msg.attach(MIMEText(html, 'html'))

server = smtplib.SMTP('smtp.gmail.com', 587)

server.starttls()
server.login(remitente, os.getenv('PASS'))

server.sendmail(remitente, destinatario, msg.as_string())
server.quit()


def enviarEmail(destinatario, asunto):
    pass
    