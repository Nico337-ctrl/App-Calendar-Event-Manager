import pywhatkit


def enviarMensajeWhats(numero, mensaje):
    pywhatkit.sendwhatmsg_instantly(numero, mensaje)